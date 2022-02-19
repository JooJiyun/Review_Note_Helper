# -*- coding: utf-8 -*-
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets

from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class MainSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.grade_in_review = '중1'
        self.student_name_in_review = ''
        self.path_collection_in_add_collection = ''

        self.make_pdf = MakePdf()
        
        self.loadData()
        self.initUi()
    
    def loadData(self):
        except_flg = False
        try:
            self.df_student_info = pd.read_csv('./student_info.csv')
        except:
            self.df_student_info = pd.DataFrame(columns = ['grade', 'student_name'])
            except_flg = True
        try:
            self.df_review_info = pd.read_csv('./review_info.csv')
        except:
            self.df_review_info = pd.DataFrame(columns=['grade', 'student_name', 'date', 'problem_id', 'problem_name', 'numbers'])
            except_flg = True
        try:
            self.df_problem_collection_info = pd.read_csv('./problem_collection_info.csv')
        except:
            self.df_problem_collection_info = pd.DataFrame(columns = ['problem_id', 'date', 'grade', 'problem_name', 'path'])  
            except_flg = True
        if except_flg:
            self.saveData()
    
    def saveData(self):
        try:
            self.df_student_info.to_csv('student_info.csv', mode = 'w', index = False)
        except:
            print('fail to save student data')
        try:
            self.df_review_info.to_csv('review_info.csv', mode = 'w', index = False)
        except:
            print('fail to save review data')
        try:
            self.df_problem_collection_info.to_csv('problem_collection_info.csv', mode = 'w', index = False)
        except:
            print('fail to save problem data')
            
    def initUi(self):
        self.setWindowTitle('오답노트 관리')
        self.setGeometry(50,50,800,500)
        
        self.tabs = QTabWidget()
        
        self.tab_review_info = self.createTabReview()
        self.tabs.addTab(self.tab_review_info, '오답노트')
        
        self.tab_problem_collection = self.createTabProblemCollection()
        self.tabs.addTab(self.tab_problem_collection, '문제지관리')
        
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.tabs)
        
        self.setLayout(self.layout_main)
        self.show()
    
    def createTabReview(self):
        self.layout_tab_review = QVBoxLayout()
        
        # - manage student -
        #region manage student
        self.layout_manage_student = QHBoxLayout()
        
        self.label_grade_in_manage_student = QLabel('학년:', self)
        self.layout_manage_student.addWidget(self.label_grade_in_manage_student)
        
        self.combo_grade_in_manage_student = QtWidgets.QComboBox(self)
        self.combo_grade_in_manage_student.addItem('중1')
        self.combo_grade_in_manage_student.addItem('중2')
        self.combo_grade_in_manage_student.addItem('중3')
        self.combo_grade_in_manage_student.addItem('고1')
        self.combo_grade_in_manage_student.addItem('고2')
        self.combo_grade_in_manage_student.addItem('고3')
        self.combo_grade_in_manage_student.activated[str].connect(self.changeGradeInReview)
        self.layout_manage_student.addWidget(self.combo_grade_in_manage_student)
        
        self.label_name_in_manage_student = QLabel('이름:', self)
        self.layout_manage_student.addWidget(self.label_name_in_manage_student)
        
        self.combo_name_in_manage_student = QtWidgets.QComboBox(self)
        self.combo_name_in_manage_student.activated.connect(self.changeNameInReview)
        self.layout_manage_student.addWidget(self.combo_name_in_manage_student)
        
        self.btn_update_review_table = QPushButton(self)
        self.btn_update_review_table.setText('조회')
        self.btn_update_review_table.clicked.connect(self.updateReviewTable)
        self.layout_manage_student.addWidget(self.btn_update_review_table)
        
        self.btn_delete_student = QPushButton(self)
        self.btn_delete_student.setText('학생정보삭제')
        self.btn_delete_student.clicked.connect(self.deleteStudent)
        self.layout_manage_student.addWidget(self.btn_delete_student)
        
        self.layout_manage_student.addStretch()
        
        self.btn_add_student = QPushButton(self)
        self.btn_add_student.setText('학생추가등록')
        self.btn_add_student.clicked.connect(self.addStudent)
        self.layout_manage_student.addWidget(self.btn_add_student)
        
        self.widget_manage_student = QWidget()
        self.widget_manage_student.setLayout(self.layout_manage_student)
        self.layout_tab_review.addWidget(self.widget_manage_student)
        
        #endregion
        
        # - add review -
        #region add review
        self.layout_add_review = QHBoxLayout()
        
        self.label_date_in_add_review = QLabel('날짜:', self)
        self.layout_add_review.addWidget(self.label_date_in_add_review)
        
        self.date_edit_in_add_review = QDateEdit(self)
        self.date_edit_in_add_review.setDate(QDate.currentDate())
        self.date_edit_in_add_review.setMinimumDate(QDate(2000, 1, 1))
        self.date_edit_in_add_review.setMaximumDate(QDate(3000, 12, 31))
        self.layout_add_review.addWidget(self.date_edit_in_add_review)
        
        self.label_problem_id_in_add_review = QLabel('문제지:', self)
        self.layout_add_review.addWidget(self.label_problem_id_in_add_review)

        self.combo_problem_collection_in_add_review = QtWidgets.QComboBox(self)
        self.layout_add_review.addWidget(self.combo_problem_collection_in_add_review)
        
        self.label_numbers_in_add_review = QLabel('틀린문제번호:', self)
        self.layout_add_review.addWidget(self.label_numbers_in_add_review)

        self.line_edit_numbers_in_add_review = QLineEdit(self)
        self.layout_add_review.addWidget(self.line_edit_numbers_in_add_review)
        
        self.btn_add_review = QPushButton(self)
        self.btn_add_review.setText('추가')
        self.btn_add_review.clicked.connect(self.addReview)
        self.layout_add_review.addWidget(self.btn_add_review)
        
        self.layout_add_review.addStretch()
        
        self.widget_add_review = QWidget()
        self.widget_add_review.setLayout(self.layout_add_review)
        self.layout_tab_review.addWidget(self.widget_add_review)

        #endregion
        
        # - manage review -
        #region manage review
        self.layout_manage_review = QHBoxLayout()
        
        self.btn_delete_review = QPushButton(self)
        self.btn_delete_review.setText('삭제')
        self.btn_delete_review.clicked.connect(self.deleteReview)
        self.layout_manage_review.addWidget(self.btn_delete_review)
        
        self.btn_modify_numbers = QPushButton(self)
        self.btn_modify_numbers.setText('틀린번호수정')
        self.btn_modify_numbers.clicked.connect(self.modifyNumbers)
        self.layout_manage_review.addWidget(self.btn_modify_numbers)
        
        self.btn_make_file = QPushButton(self)
        self.btn_make_file.setText('오답노트생성')
        self.btn_make_file.clicked.connect(self.makeNoteFile)
        self.layout_manage_review.addWidget(self.btn_make_file)
        
        self.layout_manage_review.addStretch()
        
        self.widget_manage_review = QWidget()
        self.widget_manage_review.setLayout(self.layout_manage_review)
        self.layout_tab_review.addWidget(self.widget_manage_review)
        
        #endregion
        
        # - review table -
        #region review table
        self.layout_review_table = QHBoxLayout(self)

        self.table_review = QTableWidget()
        self.table_review.setRowCount(0)
        self.table_review.setColumnCount(5)
        self.table_review.setHorizontalHeaderLabels(('선택', '날짜', '문제지번호', '문제지이름', '틀린번호들'))
        self.table_review.setColumnWidth(0,30)
        self.table_review.horizontalHeader().setStretchLastSection(True)
        self.table_review.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.layout_review_table.addWidget(self.table_review)

        self.widget_review_table = QWidget()
        self.widget_review_table.setLayout(self.layout_review_table)

        self.scroll_area_review_table = QScrollArea()
        self.scroll_area_review_table.setWidget(self.widget_review_table)
        self.scroll_area_review_table.setWidgetResizable(True)
        
        self.layout_tab_review.addWidget(self.scroll_area_review_table)
        
        #endregion
        
        self.widget_tab_review = QWidget()
        self.widget_tab_review.setLayout(self.layout_tab_review)
        
        self.changeGradeInReview()
        self.changeNameInReview()
        
        return self.widget_tab_review
    
    def addStudent(self):
        grades = ('중1','중2','중3','고1','고2','고3')
        item_grade, ok = QInputDialog.getItem(self, '학년 선택', '추가 등록할 학생의 학년을 골라주세요.', grades, 0, False)
        if ok:
            item_name, ok = QInputDialog.getText(self, '이름 입력', '추가등록할 학생의 이름을 입력해주세요.')
            if ok:
                self.df_student_info = self.df_student_info.append({'grade':item_grade, 'student_name':item_name}, ignore_index = True)
                self.saveData()
                self.changeGradeInReview()
                self.changeNameInReview()
    
    def deleteStudent(self):
        if self.student_name_in_review == '': 
            return

        reply = QMessageBox.question(self, '학생삭제확인', '학년:'+self.grade_in_review+' 이름:'+self.student_name_in_review+' 학생의 정보를 삭제하시겠습니까?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply==QMessageBox.No:
            return

        index_drop_student = self.df_student_info[(self.df_student_info['grade']==self.grade_in_review)&(self.df_student_info['student_name']==self.student_name_in_review)].index
        self.df_student_info = self.df_student_info.drop(index_drop_student)
        
        index_drop_review = self.df_review_info[(self.df_review_info['grade']==self.grade_in_review)&(self.df_review_info['student_name']==self.student_name_in_review)].index
        self.df_review_info = self.df_review_info.drop(index_drop_review)
        
        self.saveData()
        self.changeGradeInReview()
        self.changeNameInReview()
        self.updateReviewTable()
    
    def changeGradeInReview(self):
        self.grade_in_review = self.combo_grade_in_manage_student.currentText()
        
        df_student_by_grade_in_review = self.df_student_info[self.df_student_info['grade']==self.grade_in_review]
        df_student_by_grade_in_review = df_student_by_grade_in_review.reset_index(drop = True)
        df_student_by_grade_in_review = df_student_by_grade_in_review.sort_values(by=['student_name'])
        self.combo_name_in_manage_student.clear()
        for i in range(len(df_student_by_grade_in_review)):
            self.combo_name_in_manage_student.addItem(df_student_by_grade_in_review['student_name'][i])
        if len(df_student_by_grade_in_review)==0:
            self.student_name_in_review = ''
        else:
            self.changeNameInReview()
        
        self.df_problem_collection_by_grade_in_review = self.df_problem_collection_info[self.df_problem_collection_info['grade']==self.grade_in_review]
        self.df_problem_collection_by_grade_in_review = self.df_problem_collection_by_grade_in_review.reset_index(drop = False)
        self.df_problem_collection_by_grade_in_review = self.df_problem_collection_by_grade_in_review.sort_values(by=['problem_id'], ascending=False)
        self.combo_problem_collection_in_add_review.clear()
        for i in range(len(self.df_problem_collection_by_grade_in_review)):
            self.combo_problem_collection_in_add_review.addItem('['+str(self.df_problem_collection_by_grade_in_review['problem_id'][i])+'] '+str(self.df_problem_collection_by_grade_in_review['problem_name'][i]))
    
    def changeNameInReview(self):
        self.student_name_in_review = self.combo_name_in_manage_student.currentText()
         
    def updateReviewTable(self):
        self.df_review_by_grade_name_in_review = self.df_review_info[(self.df_review_info['grade']==self.grade_in_review)&(self.df_review_info['student_name']==self.student_name_in_review)]
        self.df_review_by_grade_name_in_review = self.df_review_by_grade_name_in_review.sort_values(by=['problem_id'], ascending=True)
        self.df_review_by_grade_name_in_review = self.df_review_by_grade_name_in_review.sort_values(by=['date'], ascending=False)
        self.df_review_by_grade_name_in_review = self.df_review_by_grade_name_in_review.reset_index(drop = False)
        
        self.table_review.setRowCount(len(self.df_review_by_grade_name_in_review))
        self.checkbox_list_in_review_table = []
        for i in range(len(self.df_review_by_grade_name_in_review)):
            checkbox = QCheckBox()
            self.checkbox_list_in_review_table.append(checkbox)
            self.table_review.setCellWidget(i,0,self.checkbox_list_in_review_table[i])
            self.table_review.setItem(i,1, QTableWidgetItem(str(self.df_review_by_grade_name_in_review['date'][i])))
            self.table_review.setItem(i,2, QTableWidgetItem(str(self.df_review_by_grade_name_in_review['problem_id'][i])))
            self.table_review.setItem(i,3, QTableWidgetItem(str(self.df_review_by_grade_name_in_review['problem_name'][i])))
            self.table_review.setItem(i,4, QTableWidgetItem(str(self.df_review_by_grade_name_in_review['numbers'][i])))
            
    def addReview(self):
        add_grade = self.grade_in_review
        add_sname = self.student_name_in_review
        add_date = str(self.date_edit_in_add_review.date().toPyDate())
        idx = self.combo_problem_collection_in_add_review.currentIndex()
        pr_idx = self.df_problem_collection_by_grade_in_review['index'][idx]
        add_id = self.df_problem_collection_info['problem_id'][pr_idx]
        add_pname = self.df_problem_collection_info['problem_name'][pr_idx]
        add_nums = self.line_edit_numbers_in_add_review.text()
        self.df_review_info = self.df_review_info.append({'grade':add_grade, 'student_name':add_sname, 'date':add_date, 'problem_id':int(add_id), 'problem_name':add_pname, 'numbers':add_nums},ignore_index = True)
        self.saveData()
        self.updateReviewTable()
    
    def deleteReview(self):
        for i in range(len(self.checkbox_list_in_review_table)):
            if self.checkbox_list_in_review_table[i].isChecked():
                self.df_review_info = self.df_review_info.drop(self.df_review_by_grade_name_in_review['index'][i])
        self.saveData()
        self.updateReviewTable()
    
    def modifyNumbers(self):
        for i in range(len(self.checkbox_list_in_review_table)):
            if self.checkbox_list_in_review_table[i].isChecked():
                item_numbers, ok = QInputDialog.getText(self, '틀린문제번호수정', '['+str(i+1)+'번째행]\n바뀔 틀린문제 번호들을 입력해주세요.\n번호들을 ,로 구분지어주세요.')
                if ok:
                    self.df_review_info.loc[self.df_review_by_grade_name_in_review['index'][i], 'numbers'] = item_numbers
                    self.saveData()
                    self.updateReviewTable()                
        
    def makeNoteFile(self):
        item_file_name, ok = QInputDialog.getText(self, '파일이름입력', '만들어질 파일의 이름을 입력해주세요.')
        if ok:
            self.make_pdf.totalClear()
            self.make_pdf.setSaveName(item_file_name)
            for i in range(len(self.checkbox_list_in_review_table)):
                if self.checkbox_list_in_review_table[i].isChecked():
                    problem_id = self.df_review_info['problem_id'][self.df_problem_collection_by_grade_in_review['index'][i]]
                    path_df = self.df_problem_collection_info[self.df_problem_collection_info['problem_id']==problem_id]['path']
                    path_df = path_df.reset_index(drop = True)
                    path = path_df[0]
                    numbers = self.df_review_info['numbers'][self.df_problem_collection_by_grade_in_review['index'][i]]
                    self.make_pdf.addData(path,numbers)
            QMessageBox.warning(self,'잠시만기다려주세요','파일 생성까지 시간이 조금 걸립니다. 기다려주세요.')
            self.make_pdf.savePdf()
            QMessageBox.about(self,'파일생성완료','파일이 생성되었습니다.')
                    
    
    def createTabProblemCollection(self):
        self.layout_tab_problem_collection = QVBoxLayout()
        
        # - add problem collection -
        #region add problem collection
        self.layout_add_collection = QHBoxLayout()
        
        self.combo_grade_in_add_collection = QtWidgets.QComboBox(self)
        self.combo_grade_in_add_collection.addItem('중1')
        self.combo_grade_in_add_collection.addItem('중2')
        self.combo_grade_in_add_collection.addItem('중3')
        self.combo_grade_in_add_collection.addItem('고1')
        self.combo_grade_in_add_collection.addItem('고2')
        self.combo_grade_in_add_collection.addItem('고3')
        self.layout_add_collection.addWidget(self.combo_grade_in_add_collection)
        
        self.label_date_in_add_collection = QLabel('날짜:', self)
        self.layout_add_collection.addWidget(self.label_date_in_add_collection)
        
        self.date_edit_in_add_collection = QDateEdit(self)
        self.date_edit_in_add_collection.setDate(QDate.currentDate())
        self.date_edit_in_add_collection.setMinimumDate(QDate(2000, 1, 1))
        self.date_edit_in_add_collection.setMaximumDate(QDate(3000, 12, 31))
        self.layout_add_collection.addWidget(self.date_edit_in_add_collection)
        
        self.label_problem_name_in_add_collection = QLabel('문제지 이름:', self)
        self.layout_add_collection.addWidget(self.label_problem_name_in_add_collection)
        
        self.line_edit_file_name_in_add_collection = QLineEdit(self)
        self.layout_add_collection.addWidget(self.line_edit_file_name_in_add_collection)
        
        self.layout_add_collection.addStretch()
        
        self.widget_add_collection = QWidget()
        self.widget_add_collection.setLayout(self.layout_add_collection)
        
        self.layout_tab_problem_collection.addWidget(self.widget_add_collection)
        
        # path layout separated
        self.layout_add_collection_path = QHBoxLayout()
        
        self.label_path_in_add_collection = QLabel('문제지 경로:', self)
        self.layout_add_collection_path.addWidget(self.label_path_in_add_collection)
        
        self.btn_search_file = QPushButton(self)
        self.btn_search_file.setText('문제파일검색')
        self.btn_search_file.clicked.connect(self.searchFile)
        self.layout_add_collection_path.addWidget(self.btn_search_file)
        
        self.layout_add_collection_path.addStretch()
        
        self.label_file_in_add_collection = QLabel('선택된 파일 없음',self)
        self.layout_add_collection_path.addWidget(self.label_file_in_add_collection)
        
        self.btn_add_collection = QPushButton(self)
        self.btn_add_collection.setText('문제파일추가')
        self.btn_add_collection.clicked.connect(self.addProblemCollectionFile)
        self.layout_add_collection_path.addWidget(self.btn_add_collection)
        
        self.widget_add_collection_path = QWidget()
        self.widget_add_collection_path.setLayout(self.layout_add_collection_path)
        
        self.layout_tab_problem_collection.addWidget(self.widget_add_collection_path)
        
        #endregion
        
        # - manage collection -
        #region manage collection
        self.layout_manage_collection = QHBoxLayout()
        
        self.label_grade_in_manage_collection = QLabel('학년',self)
        self.layout_manage_collection.addWidget(self.label_grade_in_manage_collection)
        
        self.combo_grade_in_manage_collection = QtWidgets.QComboBox(self)
        self.combo_grade_in_manage_collection.addItem('선택안함')
        self.combo_grade_in_manage_collection.addItem('중1')
        self.combo_grade_in_manage_collection.addItem('중2')
        self.combo_grade_in_manage_collection.addItem('중3')
        self.combo_grade_in_manage_collection.addItem('고1')
        self.combo_grade_in_manage_collection.addItem('고2')
        self.combo_grade_in_manage_collection.addItem('고3')
        self.layout_manage_collection.addWidget(self.combo_grade_in_manage_collection)
        
        self.btn_seach_collection = QPushButton(self)
        self.btn_seach_collection.setText('문제지조회')
        self.btn_seach_collection.clicked.connect(self.updateCollectionTable)
        self.layout_manage_collection.addWidget(self.btn_seach_collection)
        
        self.btn_delete_collection = QPushButton(self)
        self.btn_delete_collection.setText('문제지삭제')
        self.btn_delete_collection.clicked.connect(self.deleteCollection)
        self.layout_manage_collection.addWidget(self.btn_delete_collection)
        
        self.layout_manage_collection.addStretch()

        self.widget_manage_collection = QWidget()
        self.widget_manage_collection.setLayout(self.layout_manage_collection)
        
        self.layout_tab_problem_collection.addWidget(self.widget_manage_collection)

        #endregion

        # - collection table -
        #region collection table
        self.layout_collection_table = QHBoxLayout(self)
        
        self.table_collection = QTableWidget()
        self.table_collection.setRowCount(0)
        self.table_collection.setColumnCount(5)
        self.table_collection.setHorizontalHeaderLabels(('선택', '날짜', '문제지번호', '문제지이름', '문제지경로'))
        self.table_collection.setColumnWidth(0,30)
        self.table_collection.horizontalHeader().setStretchLastSection(True)
        #self.table_manage_pr.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_collection.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.layout_collection_table.addWidget(self.table_collection)

        self.widget_collection_table = QWidget()
        self.widget_collection_table.setLayout(self.layout_collection_table)
        
        self.scroll_area_collection_table = QScrollArea()
        self.scroll_area_collection_table.setWidget(self.widget_collection_table)
        self.scroll_area_collection_table.setWidgetResizable(True)
        
        self.layout_tab_problem_collection.addWidget(self.scroll_area_collection_table)
        
        #endregion
        
        self.widget_tab_problem_collection = QWidget()
        self.widget_tab_problem_collection.setLayout(self.layout_tab_problem_collection)
        
        return self.widget_tab_problem_collection
    
    def searchFile(self):
        f_path = QFileDialog.getOpenFileName(self)
        self.label_file_in_add_collection.setText(f_path[0])
        self.path_collection_in_add_collection = f_path[0]
    
    def addProblemCollectionFile(self):
        if self.path_collection_in_add_collection=='':
            QMessageBox.about(self, '파일추가불가', '선택된 문제파일이 없습니다.')
            return

        add_id = 1
        if len(self.df_problem_collection_info) > 0: 
            add_id = int(max(self.df_problem_collection_info['problem_id']))+1
        add_date = str(self.date_edit_in_add_collection.date().toPyDate())
        add_grade = self.combo_grade_in_add_collection.currentText()
        add_pname = self.line_edit_file_name_in_add_collection.text()
        add_path = self.path_collection_in_add_collection
        self.df_problem_collection_info = self.df_problem_collection_info.append({'problem_id':int(add_id), 'date':add_date, 'grade':add_grade, 'problem_name':add_pname, 'path':add_path}, ignore_index = True)
        self.saveData()
        self.updateCollectionTable()
        self.changeGradeInReview()
        QMessageBox.about(self,'파일추가완료','파일추가가 완료되었습니다.')
        
    def updateCollectionTable(self):
        self.df_problem_collection_by_grade_name = self.df_problem_collection_info[self.df_problem_collection_info['grade']==self.combo_grade_in_manage_collection.currentText()]
        self.df_problem_collection_by_grade_name = self.df_problem_collection_by_grade_name.sort_values(by=['date'], ascending=False)
        self.df_problem_collection_by_grade_name = self.df_problem_collection_by_grade_name.reset_index(drop = False)
        
        self.table_collection.setRowCount(len(self.df_problem_collection_by_grade_name))
        self.checkbox_list_in_collection_table = []
        for i in range(len(self.df_problem_collection_by_grade_name)):
            checkbox = QCheckBox()
            self.checkbox_list_in_collection_table.append(checkbox)
            self.table_collection.setCellWidget(i,0,self.checkbox_list_in_collection_table[i])
            self.table_collection.setItem(i,1, QTableWidgetItem(str(self.df_problem_collection_by_grade_name['date'][i])))
            self.table_collection.setItem(i,2, QTableWidgetItem(str(self.df_problem_collection_by_grade_name['problem_id'][i])))
            self.table_collection.setItem(i,3, QTableWidgetItem(str(self.df_problem_collection_by_grade_name['problem_name'][i])))
            self.table_collection.setItem(i,4, QTableWidgetItem(str(self.df_problem_collection_by_grade_name['path'][i])))
        
    def deleteCollection(self):
        reply = QMessageBox.question(self, '문제지제거', '해당 문제지들을 삭제하면 학생들의 기록에서도 해당 문제집과 관련된 기록은 모두 삭제됩니다. 삭제하시겠습니까?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply==QMessageBox.No:
            return
        for i in range(len(self.checkbox_list_in_collection_table)):
            if self.checkbox_list_in_collection_table[i].isChecked():
                delete_problem_id = self.df_problem_collection_info["problem_id"][self.df_problem_collection_by_grade_name['index'][i]]
                self.df_review_info = self.df_review_info[self.df_review_info["problem_id"]!=delete_problem_id]
                self.df_problem_collection_info = self.df_problem_collection_info.drop(self.df_problem_collection_by_grade_name['index'][i])
        self.saveData()
        self.updateCollectionTable()


class MakePdf():
    def __init__(self):
        self.totalClear()
        # pdf image size : (2339, 1653)
        # 2 line format
        self.number_y_pos = [[80, 130], [850, 900]]
        self.problem_y_pos = [[145, 795],[920, 1570]]
        self.save_name = '오답노트'
    
    def totalClear(self):
        self.result_images = []
        self.total_numbers = []
        self.total_path = []
        self.total_problem_cnt = 0
    
    def savePdf(self):
        self.getPdfResult()
        for i in range(len(self.result_images)):
            self.result_images[i] = self.result_images[i].resize((1653,2339)).convert('RGB')
            draw = ImageDraw.Draw(self.result_images[i])
            draw.text((120,45), self.save_name, font=ImageFont.truetype("NotoSansKR-Regular.otf", 45), fill=(0,0,0))
            draw.text((800,2230), '-'+str(i+1)+'-', font=ImageFont.truetype("NotoSansKR-Regular.otf", 25), fill=(0,0,0))
            draw.line((60, 120, 1593, 120), fill="black", width=5)
            draw.line((60, 2280, 1593, 2280), fill="black", width=3)
        self.result_images[0].save(self.save_name+'.pdf', resolution = 200, save_all=True, append_images=self.result_images[1:])
    
    def addData(self, add_path, add_numbers_str):
        add_numbers = add_numbers_str.split(',')
        for i in range(len(add_numbers)):
            add_numbers[i] = int(add_numbers[i])
        self.total_problem_cnt+=len(add_numbers)
        self.total_path.append(add_path)
        self.total_numbers.append(add_numbers)
    
    def setSaveName(self, save_str):
        self.save_name = save_str
    
    def getPdfResult(self):
        self.result_images = []
        total_page = int(self.total_problem_cnt/4)
        if (self.total_problem_cnt%4) != 0:
            total_page+=1
        for i in range(total_page):
            #img_data = np.zeros([32,32,3], dtype = np.uint8)
            #img_data[:,:] = [255,255,255]
            #white_img = Image.fromarray(img_data, 'RGB')
            white_img = Image.new('RGB',(1653, 2339), (255,255,255))
            self.result_images.append(white_img)
            
        current_problem_cnt = 0
        for i in range(len(self.total_path)):
            img_list = self.slicePdf(self.total_path[i], self.total_numbers[i])
            for img_idx in range(len(img_list)):
                paste_page = int(current_problem_cnt/4)
                paste_pos = int(current_problem_cnt)%4
                if paste_pos==0:
                    paste_area = (self.problem_y_pos[0][0], 150)
                    draw_pos = (self.number_y_pos[0][0], 150)
                elif paste_pos==1:
                    paste_area = (self.problem_y_pos[0][0], 1179)
                    draw_pos = (self.number_y_pos[0][0], 1179)
                elif paste_pos==2:
                    paste_area = (self.problem_y_pos[1][0], 150)
                    draw_pos = (self.number_y_pos[1][0], 150)
                else:
                    paste_area = (self.problem_y_pos[1][0], 1179)
                    draw_pos = (self.number_y_pos[1][0], 1179)
                self.result_images[paste_page].paste(img_list[img_idx], paste_area)
                current_problem_cnt+=1
                draw=ImageDraw.Draw(self.result_images[paste_page]) 
                draw.text(draw_pos, str(current_problem_cnt),font=ImageFont.truetype("NotoSansKR-Regular.otf", 42), fill=(0,0,0))
        
        return self.result_images
                
    def slicePdf(self, pdf_path, numbers):
        try:
            pdf_images = convert_from_path(pdf_path)
        except:
            print('fail to convert pdf to image')
        
        result_crop_images = []
        problem_idx = 0
        
        for i in range(len(pdf_images)):
            pdf_images[i] = pdf_images[i].resize((1653,2339))
            np_image = np.array(pdf_images[i])
        
            head_line_x_pos = 0
            tail_line_x_pos = len(np_image)-1
            mid_line_y_pos = int(len(np_image[0])/2)
            mid_line_width = 50
        
            for x_pos in range(int(len(np_image)/4)):
                flg_is_head_line = True
                for y_pos in range(mid_line_y_pos - mid_line_width, mid_line_y_pos + mid_line_width):
                    if (np_image[x_pos][y_pos]==[255,255,255]).all() == True:
                        flg_is_head_line = False
                        break
                if flg_is_head_line:
                    head_line_x_pos = x_pos
                
            for x_pos in range(len(np_image)-1, int(len(np_image)*3/4), -1):
                flg_is_tail_line = True
                for y_pos in range(mid_line_y_pos-mid_line_width, mid_line_y_pos+mid_line_width):
                    if (np_image[x_pos][y_pos]==[255,255,255]).all() == True:
                        flg_is_tail_line = False
                        break
                if flg_is_tail_line:
                    tail_line_x_pos = x_pos
        
            for line in range(len(self.problem_y_pos)):
                problem_start_x_pos = []
                problem_end_x_pos = []
                x_pos = head_line_x_pos+20
                while x_pos<tail_line_x_pos-20:
                    for y_pos in range(self.number_y_pos[line][0], self.number_y_pos[line][1]):
                        if (np_image[x_pos][y_pos]==[255,255,255]).all() == True:
                            continue
                        else:
                            if len(problem_start_x_pos)>len(problem_end_x_pos):
                                problem_end_x_pos.append(x_pos)
                            flg_real_number = True
                            for inside_y_pos in range(self.number_y_pos[line][1], self.problem_y_pos[line][0]):
                                if (np_image[x_pos][inside_y_pos]==[255,255,255]).all() == True:
                                    continue
                                else:
                                    flg_real_number = False
                                    break
                            if flg_real_number == False:
                                continue
                            problem_start_x_pos.append(x_pos-30)
                            x_pos+=100
                            break
                    x_pos+=1
                problem_cnt = len(problem_start_x_pos)
                problem_end_x_pos.append(tail_line_x_pos-20)
                for idx in range(problem_cnt):
                    left_pos = self.problem_y_pos[line][0]
                    right_pos = self.problem_y_pos[line][1]
                    top_pos = problem_start_x_pos[idx]
                    bottom_pos = problem_end_x_pos[idx]
                    crop_image = pdf_images[i].crop((left_pos, top_pos, right_pos, bottom_pos))
                    problem_idx+=1
                    if problem_idx in numbers:
                        result_crop_images.append(crop_image)
                        if len(result_crop_images)==len(numbers):
                            return result_crop_images
                        
        return result_crop_images


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainSystem()
    sys.exit(app.exec_())