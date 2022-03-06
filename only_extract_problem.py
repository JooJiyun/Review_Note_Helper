# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QCheckBox

from pdf2image import convert_from_path
import numpy as np

class MainSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        
        self.string_year = "2022"
        self.string_month = "11"
        self.string_grade = "고3"
        self.string_level = "가"
        
        self.path_paper = ""
        self.path_explain = ""
        
        self.path_result = ""
        self.name_result = ""
        
        self.list_comment_numbers = []
        
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle('시험지 자르기 - 모의고사 수학 시험지용')
        self.setGeometry(50,50,450,200)
        
        self.widget_main = QWidget()
        self.layout_main = QVBoxLayout()
        
        self.layout_main.addWidget(self.createLayoutTargetInfo())
        
        self.label_comment = QLabel(self)
        self.label_comment.setText('문항 위에 [단답형] /[5지선다] 와 같은 문구가 있는 문항을 적어주세요. (ex. 1, 16, 29)')
        self.layout_main.addWidget(self.label_comment)
        self.line_edit_comment = QLineEdit(self)
        self.layout_main.addWidget(self.line_edit_comment)
        
        self.checkbox_copyright = QCheckBox('문제지의 첫 페이지가 저작권 안내 페이지인 경우 체크해주세요.', self)
        self.layout_main.addWidget(self.checkbox_copyright)
        
        self.layout_main.addWidget(self.createLayoutPaperSlice())
        
        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)
    
    def createLayoutTargetInfo(self):
        self.layout_target_info = QHBoxLayout()
        
        target_list = ['년도', '월', '학년', '유형']
        
        self.line_edit_target_list = []
        self.label_target_list = []
        for i in range(len(target_list)):
            line_edit_item = QLineEdit(self)
            self.line_edit_target_list.append(line_edit_item)
            self.layout_target_info.addWidget(self.line_edit_target_list[i])
            
            label_item = QLabel(self)
            label_item.setText(target_list[i])
            self.label_target_list.append(label_item)
            self.layout_target_info.addWidget(self.label_target_list[i])      
        
        self.widget_target_info = QWidget()
        self.widget_target_info.setLayout(self.layout_target_info)
        
        return self.widget_target_info
        
    def createLayoutPaperSlice(self):        
        self.layout_paper_slice = QHBoxLayout()
        
        self.label_path_paper_text = QLabel('문제지 경로:', self)
        self.layout_paper_slice.addWidget(self.label_path_paper_text)
        
        self.layout_paper_slice.addStretch()
        
        self.label_path_paper = QLabel('선택된 파일 없음',self)
        self.layout_paper_slice.addWidget(self.label_path_paper)
        
        self.btn_search_file_paper = QPushButton(self)
        self.btn_search_file_paper.setText('문제지파일검색')
        self.btn_search_file_paper.clicked.connect(self.searchFilePaper)
        self.layout_paper_slice.addWidget(self.btn_search_file_paper)
        
        self.widget_paper_slice = QWidget()
        self.widget_paper_slice.setLayout(self.layout_paper_slice)
        
        self.btn_submit_paper = QPushButton(self)
        self.btn_submit_paper.setText('자르기')
        self.btn_submit_paper.clicked.connect(self.slicePaper)
        self.layout_paper_slice.addWidget(self.btn_submit_paper)
        
        return self.widget_paper_slice
    
    def searchFilePaper(self):
        f_path = QFileDialog.getOpenFileName(self)
        self.label_path_paper.setText(f_path[0])
        self.path_paper = f_path[0]
        print('paper : '+f_path[0])
        return
    
    def createOneFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            QMessageBox.warning(self,'폴더생성오류','폴더를 생성할 수 없습니다. 입력이 올바른지 확인해주세요.')
            print ('Error: Creating directory. ' +  directory)
            return -1
        return 0
    
    def createFolders(self):
        self.string_year = self.line_edit_target_list[0].text()
        self.string_month = self.line_edit_target_list[1].text()
        self.string_grade = self.line_edit_target_list[2].text()
        self.string_level = self.line_edit_target_list[3].text()
        
        self.name_result = '/'
        self.name_result += self.string_year
        for i in range(1, 4):
            self.name_result += '-' + self.line_edit_target_list[i].text()
        
        self.path_result = ""
        self.path_result += self.string_year
        if self.createOneFolder(self.path_result)<0:
            return -1
        
        self.path_result += '/' + self.string_month
        if self.createOneFolder(self.path_result)<0:
            return -1
        
        self.path_result += '/' + self.string_grade
        if self.createOneFolder(self.path_result)<0:
            return -1
        
        self.path_result += '/' + self.string_level
        if self.createOneFolder(self.path_result)<0:
            return -1
        
        return 0
    
    def slicePaper(self):
        if self.createFolders()<0:
            return
        self.setCommentNumbers()
        QMessageBox.warning(self,'파일생성시작','파일을 만드는데 30초~3분의 시간이 걸립니다. 응답없음이 떠도 잠시만 완료 메세지가 뜰 때까지 기다려주세요.')
        if self.extractProblem() <0:
            QMessageBox.warning(self,'파일생성오류','파일을 불러올 수 없습니다. 입력을 확인해주세요.')
            return
        QMessageBox.about(self,'파일생성완료','파일이 생성되었습니다.')
        
    def sliceExplain(self):
        if self.createFolders()<0:
            return
        QMessageBox.warning(self,'파일생성시작','파일을 만드는데 시간이 걸립니다. 완료 메세지가 뜰 때까지 기다려주세요.')
        if self.extractExplain() <0:
            QMessageBox.warning(self,'파일생성오류','파일을 불러올 수 없습니다. 입력을 확인해주세요.')
            return
        QMessageBox.about(self,'파일생성완료','파일이 생성되었습니다.')
    
    def setCommentNumbers(self):
        comment_numbers = self.line_edit_comment.text().split(',')
        self.list_comment_numbers = []
        for i in range(len(comment_numbers)):
            self.list_comment_numbers.append(int(comment_numbers[i]))
    
    def extractProblem(self):
        try:
            pdf_images = convert_from_path(self.path_paper,500, size = (2339,3309))
        except:
            print('fail to convert pdf to image')
            return -1
        
        problem_no = 1
        for img_idx in range(len(pdf_images)):
            if (self.checkbox_copyright.isChecked()) & (img_idx==0):
                continue
            pdf_images[img_idx] = pdf_images[img_idx].resize((2339,3309))
            np_image = np.array(pdf_images[img_idx])
        
            head_line_x_pos = 0
            mid_line_y_pos = int(len(np_image[0])/2)
            head_mid_y_width = 50
            tail_line_x_pos = 2670
            
            for x_pos in range(100, int(len(np_image)/4)):
                flg_is_head_line = True
                for y_pos in range(mid_line_y_pos - head_mid_y_width, mid_line_y_pos + head_mid_y_width):
                    if (np_image[x_pos][y_pos]==[255,255,255]).all() == True:
                        flg_is_head_line = False
                        break
                if flg_is_head_line:
                    head_line_x_pos = x_pos + 23
            
            problem_y_pos= [[212, mid_line_y_pos - 10],[mid_line_y_pos + 10, 2128]]
            for line in range(2):
                is_next_problem = True
                x_pos = head_line_x_pos
                problem_start_x_pos = []
                problem_end_x_pos = []
                white_line_cnt = 0
                while x_pos<tail_line_x_pos:
                    x_pos+=1
                    y_pos = problem_y_pos[line][0]
                    is_white_line = False
                    while y_pos<problem_y_pos[line][1]:
                        y_pos+=10
                        if (np_image[x_pos][y_pos]==[255,255,255]).all() == True:
                            is_white_line = True
                        else:
                            is_white_line = False
                            break
                    
                    if is_white_line:
                        white_line_cnt+=1
                        if white_line_cnt>200:
                            
                            if is_next_problem==False:
                                is_next_problem = True
                                white_line_cnt = 0
                                problem_end_x_pos.append(x_pos-200)
                    else:
                        white_line_cnt = 0
                        if is_next_problem:
                            is_next_problem = False
                            problem_start_x_pos.append(x_pos)
                            x_pos+=200
                            
                problem_end_x_pos.append(tail_line_x_pos)
                
                comment_problem = self.list_comment_numbers
                for idx in range(len(problem_start_x_pos)):
                    left_pos = problem_y_pos[line][0]
                    right_pos = problem_y_pos[line][1]
                    top_pos = problem_start_x_pos[idx]
                    bottom_pos = problem_end_x_pos[idx] 
                    if problem_no in comment_problem:
                        top_pos+=90
                    crop_image = pdf_images[img_idx].crop(self.getCropAreaProblem(line, left_pos, top_pos, right_pos, bottom_pos, np_image))
                    crop_image.save(self.path_result + self.name_result+'-'+str(problem_no)+'.png')
                    problem_no+=1
        return 0
        
    def getCropAreaProblem(self, line, left_pos, top_pos, right_pos, bottom_pos, np_image):
        delta = 10
        while(bottom_pos>top_pos):
            bottom_pos-=delta
            flg_cut_area = True;
            y_pos = left_pos-10
            while y_pos < right_pos:
                y_pos+=10
                if (np_image[bottom_pos][y_pos]==[255,255,255]).all() == False:
                    flg_cut_area = False
                    break
            if flg_cut_area:
                continue
            if delta == 1:
                break
            else:
                bottom_pos+=delta
                delta = 1
        
        while(top_pos<bottom_pos):
            top_pos+=1
            flg_cut_area = True;
            white_cnt = 0
            not_white_cnt = 0
            if line==0:
                y_pos = 250
                y_pos_end = 300
            else:
                y_pos = 1240
                y_pos_end = 1300
            
            while y_pos<y_pos_end:
                y_pos+=1
                if (np_image[top_pos][y_pos]==[255,255,255]).all()==True:
                    white_cnt+=1
                else:
                    not_white_cnt+=1
            
            flg_cut_area = (white_cnt*not_white_cnt) == 0
            if flg_cut_area:
                continue
            if white_cnt==0:
                top_pos+=90
            else:
                break
        
        return (left_pos, top_pos-23, right_pos, bottom_pos+25)
    

def main():
    app = QApplication(sys.argv)
    window = MainSystem()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()