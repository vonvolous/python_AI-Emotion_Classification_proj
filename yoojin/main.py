# import modules for Calendar
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog
from PIL import ImageTk, Image

# import modules for Emotion Classification
import tensorflow as tf
import cv2
import numpy as np

# Main 화면에 캘린더 띄우기
class Agenda(Calendar):

    def __init__(self, master=None, **kw):
        Calendar.__init__(self, master, **kw)
        # change a bit the options of the labels to improve display
        for i, row in enumerate(self._calendar):
            for j, label in enumerate(row):
                self._cal_frame.rowconfigure(i + 1, uniform=1)
                self._cal_frame.columnconfigure(j + 1, uniform=1)
                label.configure(justify="center", anchor="n", padding=(1, 4))

    def _display_days_without_othermonthdays(self):
        year, month = self._date.year, self._date.month

        cal = self._cal.monthdays2calendar(year, month)
        while len(cal) < 6:
            cal.append([(0, i) for i in range(7)])

        week_days = {i: 'normal.%s.TLabel' % self._style_prefixe for i in range(7)}  # style names depending on the type of day
        week_days[self['weekenddays'][0] - 1] = 'we.%s.TLabel' % self._style_prefixe
        week_days[self['weekenddays'][1] - 1] = 'we.%s.TLabel' % self._style_prefixe
        _, week_nb, d = self._date.isocalendar()
        if d == 7 and self['firstweekday'] == 'sunday':
            week_nb += 1
        modulo = max(week_nb, 52)
        for i_week in range(6):
            if i_week == 0 or cal[i_week][0][0]:
                self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
            else:
                self._week_nbs[i_week].configure(text='')
            for i_day in range(7):
                day_number, week_day = cal[i_week][i_day]
                style = week_days[i_day]
                label = self._calendar[i_week][i_day]
                label.state(['!disabled'])
                if day_number:
                    txt = str(day_number)
                    label.configure(text=txt, style=style)
                    date = self.date(year, month, day_number)
                    if date in self._calevent_dates:
                        ev_ids = self._calevent_dates[date]
                        i = len(ev_ids) - 1
                        while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                            i -= 1
                        if i >= 0:
                            tag = self.calevents[ev_ids[i]]['tags'][-1]
                            label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
                        # modified lines:
                        text = '%s\n' % day_number + '\n'.join([self.calevents[ev]['text'] for ev in ev_ids])
                        label.configure(text=text)
                else:
                    label.configure(text='', style=style)

    def _display_days_with_othermonthdays(self):
        year, month = self._date.year, self._date.month

        cal = self._cal.monthdatescalendar(year, month)

        next_m = month + 1
        y = year
        if next_m == 13:
            next_m = 1
            y += 1
        if len(cal) < 6:
            if cal[-1][-1].month == month:
                i = 0
            else:
                i = 1
            cal.append(self._cal.monthdatescalendar(y, next_m)[i])
            if len(cal) < 6:
                cal.append(self._cal.monthdatescalendar(y, next_m)[i + 1])

        week_days = {i: 'normal' for i in range(7)}  # style names depending on the type of day
        week_days[self['weekenddays'][0] - 1] = 'we'
        week_days[self['weekenddays'][1] - 1] = 'we'
        prev_m = (month - 2) % 12 + 1
        months = {month: '.%s.TLabel' % self._style_prefixe,
                  next_m: '_om.%s.TLabel' % self._style_prefixe,
                  prev_m: '_om.%s.TLabel' % self._style_prefixe}

        week_nb = cal[0][1].isocalendar()[1]
        modulo = max(week_nb, 52)
        for i_week in range(6):
            self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
            for i_day in range(7):
                style = week_days[i_day] + months[cal[i_week][i_day].month]
                label = self._calendar[i_week][i_day]
                label.state(['!disabled'])
                txt = str(cal[i_week][i_day].day)
                label.configure(text=txt, style=style)
                if cal[i_week][i_day] in self._calevent_dates:
                    date = cal[i_week][i_day]
                    ev_ids = self._calevent_dates[date]
                    i = len(ev_ids) - 1
                    while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                        i -= 1
                    if i >= 0:
                        tag = self.calevents[ev_ids[i]]['tags'][-1]
                        label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
                    # modified lines:
                    text = '%s\n' % date.day + '\n'.join([self.calevents[ev]['text'] for ev in ev_ids])
                    label.configure(text=text)

    def _show_event(self, date):
        """Display events on date if visible."""
        w, d = self._get_day_coords(date)
        if w is not None:
            label = self._calendar[w][d]
            if not label.cget('text'):
                # this is an other month's day and showothermonth is False
                return
            ev_ids = self._calevent_dates[date]
            i = len(ev_ids) - 1
            while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                i -= 1
            if i >= 0:
                tag = self.calevents[ev_ids[i]]['tags'][-1]
                label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
            # modified lines:
            text = '%s\n' % date.day + '\n'.join([self.calevents[ev]['text'] for ev in ev_ids])
            label.configure(text=text)

if __name__ == '__main__':
    # 감정 분석 
    def emotion_classification(img_path):
        global cur_emotion
        emotion_list = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "neutral", 5: "sad", 6: "surprise"}
        
        # load the trained model
        print('\n\nmodel training...\n')
        with open('trained_network.json', 'r') as trained_network_json:
            trained_model_json = trained_network_json.read()
        
        network = tf.keras.models.model_from_json(trained_model_json)
        network.load_weights('weights_emotions.hdf5')
        network.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
        
        # inference with the input image
        image = cv2.imread(img_path)
        
        # 사진에서 얼굴 인식을 위해 haarcascade 불러오기
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 얼굴 찾기, face : top, right, bottom, left
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # crop the region of interest over a copy
        x, y, w, h = face[0]
        roi = image[y:y+h, x:x+w]
        
        # Resize image to 48, 48
        roi = cv2.resize(roi, (48, 48))
        
        # Normalize
        roi = roi / 255
        
        roi = np.expand_dims(roi, axis=0)
        pred_probability = network.predict(roi)
        pred = np.argmax(pred_probability)
        cur_emotion = emotion_list[pred]
        print('현재 감정:', cur_emotion)
        
        return cur_emotion


    # 선택된 날짜 이미지 업로드 창 띄우는 함수
    def uploading_window(e):
        selected_date = de.get_date()
        
        global picLabel, textLabel, photo, new_window
        new_window = tk.Toplevel(root)
        new_window.title(selected_date)
        new_window.geometry("300x500")
        
        # choose image button
        chooseBtn = tk.Button(new_window, text ='Choose File', command = lambda:upload_photo(selected_date)) 
        chooseBtn.grid(row=2, column=1)
        chooseBtn.pack(side="top")
        
        # show image label
        photo = tk.PhotoImage(file='initial_upload_image.png')
        picLabel = tk.Label(new_window, image=photo)
        picLabel.pack()
        
        # show emotion classification result label
        textLabel = tk.Label(new_window, text='')
        textLabel.pack()

    # uploading_window에 사진 업로드하는 함수
    def upload_photo(selected_date):
        emotion_icon = {"happy" : "\U0001f600", "sad":"\U0001F62D", "fear": "\U0001F62C", "angry": "\U0001F621", "disgust": "\U0001F92E" ,"neutral": "\U0001F610" ,"surprise": "\U0001F632"}

        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*')])
        print('파일 경로', file_path)

        # 이미지 분석 결과 아이콘을 캘린더에 삽입
        
        my_emotion = emotion_classification(file_path)
        my_emoticon = emotion_icon[my_emotion]
        agenda.calevent_create(selected_date, my_emoticon, 'emotion')
        agenda.tag_config('emotion', background='yellow', foreground='black')

        photo = Image.open(file_path, mode='r').resize((290, 290))
        picLabel.img = ImageTk.PhotoImage(photo)
        picLabel.configure(image=picLabel.img)
        textLabel.configure(text=my_emotion)
                
    
    root = tk.Tk()
    root.geometry("800x500")
    root.title("My Daily Emotion")
    
    agenda = Agenda(root, selectmode='day', cursor='hand1')
    # date = agenda.datetime.today() + agenda.timedelta(days=2)
    # agenda.calevent_create(date, 'Hello World', 'message')
    # agenda.calevent_create(date, 'Reminder 2', 'reminder')
    # agenda.calevent_create(date + agenda.timedelta(days=-7), 'Reminder 1', 'reminder')
    # agenda.calevent_create(date + agenda.timedelta(days=3), 'Message', 'message')
    # agenda.calevent_create(date + agenda.timedelta(days=3), 'Another message', 'message')

    agenda.pack(fill="both", expand=True)
    # agenda.bind("<<CalendarSelected>>", lambda event: uploading_window(agenda.get_date()))

    de = DateEntry(root, selectmode="day")
    de.pack()
    de.bind("<<DateEntrySelected>>", uploading_window)
    
    root.mainloop()  
