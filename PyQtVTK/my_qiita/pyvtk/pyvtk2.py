#!/usr/bin/env python

# -*- coding: utf-8 -*-
import sys
import vtk as vtk
from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.numpy_support import vtk_to_numpy


class MainWindow(Qt.QMainWindow):

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        # Qtの枠の設定
        self.setWindowTitle('QtSample')

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.iren = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.iren)
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.rootDir = "C:/Shaohui/OpenFoam/radiationTest/air99surf"
        self.fileName = self.rootDir + "/system/controlDict"

        # reader
        self.reader = vtk.vtkOpenFOAMReader()
        self.reader.SetFileName(self.fileName)
        self.reader.CreateCellToPointOn()
        self.reader.DecomposePolyhedraOn()
        self.reader.EnableAllCellArrays()
        self.reader.Update()

        tArray = vtk_to_numpy(self.reader.GetTimeValues())  # 出力ファイルの時間を格納
        self.reader.UpdateTimeStep(tArray[1])  # 最新の時間406を出力設定
        print(tArray)
        self.reader.Update()

        self.filter = vtk.vtkGeometryFilter()
        self.filter.SetInputConnection(self.reader.GetOutputPort())  # filterにreaderを設定

        # mapper



        self.mapper = vtk.vtkCompositePolyDataMapper2()
        self.mapper.SetInputConnection(self.filter.GetOutputPort())  # mapperにfilterを設定
        # スカラー値の設定
        self.mapper.SetScalarModeToUseCellFieldData()  # scalarデータ用に設定
        self.mapper.SelectColorArray("p")  # 圧力を表示する
        self.mapper.SetScalarRange(-10, 50)  # 圧力を[-10,50]の範囲で表示

        # actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)  # actorにmapperを設定

        # renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)  # rendererにactorを設定

        # 背景色の設定
        self.renderer.GradientBackgroundOn()  # グラデーション背景を設定
        self.renderer.SetBackground2(0.2, 0.4, 0.6)  # 上面の色
        self.renderer.SetBackground(1, 1, 1)  # 下面の色

        # Window
        self.iren.GetRenderWindow().AddRenderer(self.renderer)
        self.iren.SetSize(850, 850)
        self.iren.Initialize()
        self.iren.Start()
        self.show()


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
