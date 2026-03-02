import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QFrame, QScrollArea, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from qfluentwidgets import (
    SubtitleLabel, BodyLabel, StrongBodyLabel,
    PushButton, PrimaryPushButton, ComboBox, LineEdit, TextEdit,
    CheckBox, RadioButton, CardWidget,
    FluentIcon as FIF, InfoBar, InfoBarPosition,
    ListWidget
)


class WorkflowItem:
    def __init__(self, config=None):
        self.config = config or {
            "title": "提示",
            "content": "这是一个弹窗",
            "icon": "info",
            "buttons": "ok",
            "style": 0,
            "theme": 0,
            "inputOptions": {
                "hasInput": False,
                "inputPlaceholder": "请输入内容...",
                "hasRadio": False,
                "radioOptions": ["选项1", "选项2", "选项3"],
                "hasCheck": False,
                "checkOptions": ["选项A", "选项B", "选项C"]
            }
        }


class WorkflowModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workflowItems = []
        self.currentItemIndex = -1
        self._initUI()
        
    def _initUI(self):
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)
        
        leftPanel = self._createLeftPanel()
        mainLayout.addWidget(leftPanel, 1)
        
        rightPanel = self._createRightPanel()
        mainLayout.addWidget(rightPanel, 2)
        
    def _createLeftPanel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        titleCard = CardWidget()
        titleLayout = QHBoxLayout(titleCard)
        titleLayout.setContentsMargins(20, 15, 20, 15)
        titleLayout.addWidget(SubtitleLabel("工作流"))
        titleLayout.addStretch()
        layout.addWidget(titleCard)
        
        listCard = CardWidget()
        listLayout = QVBoxLayout(listCard)
        listLayout.setContentsMargins(15, 15, 15, 15)
        listLayout.setSpacing(10)
        
        self.workflowList = ListWidget()
        self.workflowList.setFixedHeight(400)
        self.workflowList.currentRowChanged.connect(self._onItemSelected)
        listLayout.addWidget(self.workflowList)
        
        btnLayout = QHBoxLayout()
        
        addBtn = PushButton("添加")
        addBtn.setIcon(FIF.ADD)
        addBtn.clicked.connect(self._addItem)
        btnLayout.addWidget(addBtn)
        
        removeBtn = PushButton("删除")
        removeBtn.setIcon(FIF.REMOVE)
        removeBtn.clicked.connect(self._removeItem)
        btnLayout.addWidget(removeBtn)
        
        upBtn = PushButton("上移")
        upBtn.setIcon(FIF.UP)
        upBtn.clicked.connect(self._moveUp)
        btnLayout.addWidget(upBtn)
        
        downBtn = PushButton("下移")
        downBtn.setIcon(FIF.DOWN)
        downBtn.clicked.connect(self._moveDown)
        btnLayout.addWidget(downBtn)
        
        listLayout.addLayout(btnLayout)
        layout.addWidget(listCard)
        
        actionCard = CardWidget()
        actionLayout = QVBoxLayout(actionCard)
        actionLayout.setContentsMargins(15, 15, 15, 15)
        actionLayout.setSpacing(10)
        
        actionLayout.addWidget(StrongBodyLabel("工作流操作"))
        
        saveBtn = PushButton("保存工作流")
        saveBtn.setIcon(FIF.SAVE)
        saveBtn.clicked.connect(self._saveWorkflow)
        actionLayout.addWidget(saveBtn)
        
        loadBtn = PushButton("加载工作流")
        loadBtn.setIcon(FIF.FOLDER)
        loadBtn.clicked.connect(self._loadWorkflow)
        actionLayout.addWidget(loadBtn)
        
        exportBtn = PrimaryPushButton("导出工作流脚本")
        exportBtn.setIcon(FIF.SHARE)
        exportBtn.clicked.connect(self._exportWorkflow)
        actionLayout.addWidget(exportBtn)
        
        layout.addWidget(actionCard)
        layout.addStretch()
        
        return panel
        
    def _createRightPanel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        self.editCard = CardWidget()
        self.editLayout = QVBoxLayout(self.editCard)
        self.editLayout.setContentsMargins(20, 20, 20, 20)
        self.editLayout.setSpacing(15)
        
        self.editLayout.addWidget(StrongBodyLabel("编辑弹窗"))
        
        self.editLayout.addWidget(BodyLabel("标题:"))
        self.titleEdit = LineEdit()
        self.titleEdit.setPlaceholderText("输入弹窗标题")
        self.titleEdit.textChanged.connect(self._updateCurrentItem)
        self.editLayout.addWidget(self.titleEdit)
        
        self.editLayout.addWidget(BodyLabel("内容:"))
        self.contentEdit = TextEdit()
        self.contentEdit.setPlaceholderText("输入弹窗内容")
        self.contentEdit.setFixedHeight(80)
        self.contentEdit.textChanged.connect(self._updateCurrentItem)
        self.editLayout.addWidget(self.contentEdit)
        
        iconRow = QHBoxLayout()
        iconRow.addWidget(BodyLabel("图标:"))
        self.iconCombo = ComboBox()
        self.iconCombo.addItems(["警告", "提示", "错误", "疑问", "成功", "无图标"])
        self.iconCombo.currentIndexChanged.connect(self._updateCurrentItem)
        iconRow.addWidget(self.iconCombo)
        iconRow.addStretch()
        self.editLayout.addLayout(iconRow)
        
        btnRow = QHBoxLayout()
        btnRow.addWidget(BodyLabel("按钮:"))
        self.btnCombo = ComboBox()
        self.btnCombo.addItems(["确定", "确定/取消", "是/否", "是/否/取消", "重试/取消", "中止/重试/忽略"])
        self.btnCombo.currentIndexChanged.connect(self._updateCurrentItem)
        btnRow.addWidget(self.btnCombo)
        btnRow.addStretch()
        self.editLayout.addLayout(btnRow)
        
        styleRow = QHBoxLayout()
        styleRow.addWidget(BodyLabel("样式:"))
        self.styleCombo = ComboBox()
        self.styleCombo.addItems(["WinUI", "MessageBox", "ContentDialog"])
        self.styleCombo.currentIndexChanged.connect(self._updateCurrentItem)
        styleRow.addWidget(self.styleCombo)
        styleRow.addStretch()
        self.editLayout.addLayout(styleRow)
        
        self.editLayout.addWidget(CheckBox("显示输入框"))
        self.hasInputCheck = self.editLayout.itemAt(self.editLayout.count() - 1).widget()
        self.hasInputCheck.stateChanged.connect(self._updateCurrentItem)
        
        self.editLayout.addWidget(CheckBox("显示单选按钮"))
        self.hasRadioCheck = self.editLayout.itemAt(self.editLayout.count() - 1).widget()
        self.hasRadioCheck.stateChanged.connect(self._updateCurrentItem)
        
        self.editLayout.addWidget(CheckBox("显示复选框"))
        self.hasCheckCheck = self.editLayout.itemAt(self.editLayout.count() - 1).widget()
        self.hasCheckCheck.stateChanged.connect(self._updateCurrentItem)
        
        self.editCard.setEnabled(False)
        layout.addWidget(self.editCard)
        layout.addStretch()
        
        scroll.setWidget(panel)
        return scroll
        
    def _addItem(self):
        item = WorkflowItem()
        self.workflowItems.append(item)
        listItem = QListWidgetItem(f"弹窗 {len(self.workflowItems)}")
        self.workflowList.addItem(listItem)
        self.workflowList.setCurrentRow(len(self.workflowItems) - 1)
        
    def _removeItem(self):
        currentRow = self.workflowList.currentRow()
        if currentRow >= 0:
            self.workflowList.takeItem(currentRow)
            del self.workflowItems[currentRow]
            self._updateListLabels()
            
    def _moveUp(self):
        currentRow = self.workflowList.currentRow()
        if currentRow > 0:
            self.workflowItems[currentRow], self.workflowItems[currentRow - 1] = \
                self.workflowItems[currentRow - 1], self.workflowItems[currentRow]
            self._updateListLabels()
            self.workflowList.setCurrentRow(currentRow - 1)
            
    def _moveDown(self):
        currentRow = self.workflowList.currentRow()
        if currentRow >= 0 and currentRow < len(self.workflowItems) - 1:
            self.workflowItems[currentRow], self.workflowItems[currentRow + 1] = \
                self.workflowItems[currentRow + 1], self.workflowItems[currentRow]
            self._updateListLabels()
            self.workflowList.setCurrentRow(currentRow + 1)
            
    def _updateListLabels(self):
        for i in range(self.workflowList.count()):
            self.workflowList.item(i).setText(f"弹窗 {i + 1}")
            
    def _onItemSelected(self, index):
        self.currentItemIndex = index
        if index >= 0 and index < len(self.workflowItems):
            self.editCard.setEnabled(True)
            item = self.workflowItems[index]
            config = item.config
            
            self.titleEdit.setText(config.get("title", ""))
            self.contentEdit.setText(config.get("content", ""))
            
            iconMap = {"warning": 0, "info": 1, "error": 2, "question": 3, "success": 4, "none": 5}
            self.iconCombo.setCurrentIndex(iconMap.get(config.get("icon", "info"), 1))
            
            btnMap = {"ok": 0, "ok_cancel": 1, "yes_no": 2, "yes_no_cancel": 3, "retry_cancel": 4, "abort_retry_ignore": 5}
            self.btnCombo.setCurrentIndex(btnMap.get(config.get("buttons", "ok"), 0))
            
            self.styleCombo.setCurrentIndex(config.get("style", 0))
            
            inputOpts = config.get("inputOptions", {})
            self.hasInputCheck.setChecked(inputOpts.get("hasInput", False))
            self.hasRadioCheck.setChecked(inputOpts.get("hasRadio", False))
            self.hasCheckCheck.setChecked(inputOpts.get("hasCheck", False))
        else:
            self.editCard.setEnabled(False)
            
    def _updateCurrentItem(self):
        if self.currentItemIndex >= 0 and self.currentItemIndex < len(self.workflowItems):
            item = self.workflowItems[self.currentItemIndex]
            
            iconList = ["warning", "info", "error", "question", "success", "none"]
            btnList = ["ok", "ok_cancel", "yes_no", "yes_no_cancel", "retry_cancel", "abort_retry_ignore"]
            
            item.config = {
                "title": self.titleEdit.text(),
                "content": self.contentEdit.toPlainText(),
                "icon": iconList[self.iconCombo.currentIndex()],
                "buttons": btnList[self.btnCombo.currentIndex()],
                "style": self.styleCombo.currentIndex(),
                "theme": 0,
                "inputOptions": {
                    "hasInput": self.hasInputCheck.isChecked(),
                    "inputPlaceholder": "请输入内容...",
                    "hasRadio": self.hasRadioCheck.isChecked(),
                    "radioOptions": ["选项1", "选项2", "选项3"],
                    "hasCheck": self.hasCheckCheck.isChecked(),
                    "checkOptions": ["选项A", "选项B", "选项C"]
                }
            }
            
    def _saveWorkflow(self):
        if not self.workflowItems:
            InfoBar.warning(
                title="无法保存",
                content="工作流为空，请先添加弹窗",
                parent=self.window(),
                duration=2000
            )
            return
            
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "保存工作流",
            "",
            "WindowMatter 工作流 (*.winwf)"
        )
        
        if filePath:
            if not filePath.endswith(".winwf"):
                filePath += ".winwf"
            try:
                workflowData = {
                    "version": "1.0",
                    "items": [item.config for item in self.workflowItems]
                }
                with open(filePath, "w", encoding="utf-8") as f:
                    json.dump(workflowData, f, ensure_ascii=False, indent=2)
                InfoBar.success(
                    title="保存成功",
                    content=f"工作流已保存到: {filePath}",
                    parent=self.window(),
                    duration=3000
                )
            except Exception as e:
                InfoBar.error(
                    title="保存失败",
                    content=str(e),
                    parent=self.window(),
                    duration=3000
                )
                
    def _loadWorkflow(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "加载工作流",
            "",
            "WindowMatter 工作流 (*.winwf)"
        )
        
        if filePath:
            try:
                with open(filePath, "r", encoding="utf-8") as f:
                    workflowData = json.load(f)
                
                self.workflowItems = []
                self.workflowList.clear()
                
                for itemConfig in workflowData.get("items", []):
                    item = WorkflowItem(itemConfig)
                    self.workflowItems.append(item)
                    listItem = QListWidgetItem(f"弹窗 {len(self.workflowItems)}")
                    self.workflowList.addItem(listItem)
                
                InfoBar.success(
                    title="加载成功",
                    content=f"工作流已从 {filePath} 加载",
                    parent=self.window(),
                    duration=3000
                )
            except Exception as e:
                InfoBar.error(
                    title="加载失败",
                    content=str(e),
                    parent=self.window(),
                    duration=3000
                )
                
    def _exportWorkflow(self):
        if not self.workflowItems:
            InfoBar.warning(
                title="无法导出",
                content="工作流为空，请先添加弹窗",
                parent=self.window(),
                duration=2000
            )
            return
            
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "导出工作流脚本",
            "workflow.py",
            "Python 文件 (*.py)"
        )
        
        if filePath:
            try:
                script = self._generateWorkflowScript()
                with open(filePath, "w", encoding="utf-8") as f:
                    f.write(script)
                InfoBar.success(
                    title="导出成功",
                    content=f"工作流脚本已保存到: {filePath}",
                    parent=self.window(),
                    duration=3000
                )
            except Exception as e:
                InfoBar.error(
                    title="导出失败",
                    content=str(e),
                    parent=self.window(),
                    duration=3000
                )
                
    def _generateWorkflowScript(self):
        script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WindowMatter 自动生成的工作流脚本

import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QRadioButton, QCheckBox, QButtonGroup, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

'''
        
        for i, item in enumerate(self.workflowItems):
            config = item.config
            script += self._generateDialogClass(i, config)
            script += "\n"
            
        script += '''
def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 10))
    
    results = []
'''
        
        for i in range(len(self.workflowItems)):
            script += f'''
    dialog{i} = PopupDialog{i}()
    result{i} = dialog{i}.exec()
    if result{i} == QDialog.Accepted:
        results.append(dialog{i}.getResult())
    else:
        print("用户在第{i+1}个弹窗取消了操作")
        return
'''
        
        script += '''
    print("所有弹窗完成!")
    print("结果:", results)
    return 0

if __name__ == '__main__':
    sys.exit(main())
'''
        return script
        
    def _generateDialogClass(self, index, config):
        icon_map = {
            "warning": "⚠️",
            "info": "ℹ️",
            "error": "❌",
            "question": "❓",
            "success": "✅",
            "none": ""
        }
        icon_text = icon_map.get(config.get("icon", "info"), "ℹ️")
        
        className = f"PopupDialog{index}"
        
        script = f'''class {className}(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle({repr(config.get("title", "提示"))})
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标和内容
        headerLayout = QHBoxLayout()
'''
        
        if icon_text:
            script += f'''        iconLabel = QLabel("{icon_text}")
        iconLabel.setStyleSheet("font-size: 32px;")
        headerLayout.addWidget(iconLabel)
'''
        
        script += f'''        contentLabel = QLabel({repr(config.get("content", ""))})
        contentLabel.setWordWrap(True)
        contentLabel.setStyleSheet("font-size: 14px;")
        headerLayout.addWidget(contentLabel, 1)
        layout.addLayout(headerLayout)
'''
        
        inputOpts = config.get("inputOptions", {})
        
        if inputOpts.get("hasInput", False):
            script += f'''
        self.inputEdit = QLineEdit()
        self.inputEdit.setPlaceholderText({repr(inputOpts.get("inputPlaceholder", "请输入内容..."))})
        layout.addWidget(self.inputEdit)
'''
        
        if inputOpts.get("hasRadio", False):
            script += '''
        self.radioGroup = QButtonGroup(self)
'''
            for j, opt in enumerate(inputOpts.get("radioOptions", [])):
                if opt.strip():
                    script += f'''        radio{j} = QRadioButton({repr(opt.strip())})
        self.radioGroup.addButton(radio{j}, {j})
        layout.addWidget(radio{j})
'''
            script += '''        if self.radioGroup.buttons():
            self.radioGroup.buttons()[0].setChecked(True)
'''
        
        if inputOpts.get("hasCheck", False):
            script += '''
        self.checkBoxes = []
'''
            for j, opt in enumerate(inputOpts.get("checkOptions", [])):
                if opt.strip():
                    script += f'''        check{j} = QCheckBox({repr(opt.strip())})
        self.checkBoxes.append(check{j})
        layout.addWidget(check{j})
'''
        
        script += '''
        # 按钮
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
'''
        
        buttons = config.get("buttons", "ok")
        if buttons == "ok":
            script += '''        okBtn = QPushButton("确定")
        okBtn.clicked.connect(self.accept)
        btnLayout.addWidget(okBtn)
'''
        elif buttons in ["ok_cancel", "yes_no", "retry_cancel"]:
            btn1_text = {"ok_cancel": "确定", "yes_no": "是", "retry_cancel": "重试"}[buttons]
            btn2_text = {"ok_cancel": "取消", "yes_no": "否", "retry_cancel": "取消"}[buttons]
            script += f'''        btn1 = QPushButton("{btn1_text}")
        btn1.clicked.connect(self.accept)
        btnLayout.addWidget(btn1)
        
        btn2 = QPushButton("{btn2_text}")
        btn2.clicked.connect(self.reject)
        btnLayout.addWidget(btn2)
'''
        else:
            script += '''        okBtn = QPushButton("确定")
        okBtn.clicked.connect(self.accept)
        btnLayout.addWidget(okBtn)
        
        cancelBtn = QPushButton("取消")
        cancelBtn.clicked.connect(self.reject)
        btnLayout.addWidget(cancelBtn)
'''
        
        script += '''        layout.addLayout(btnLayout)
    
    def getResult(self):
        result = {}
'''
        
        if inputOpts.get("hasInput", False):
            script += '''        result["input"] = self.inputEdit.text()
'''
        
        if inputOpts.get("hasRadio", False):
            script += '''        result["radio"] = self.radioGroup.checkedId() if self.radioGroup.checkedButton() else -1
'''
        
        if inputOpts.get("hasCheck", False):
            script += '''        result["checks"] = [cb.isChecked() for cb in self.checkBoxes]
'''
        
        script += '''        return result
'''
        
        return script
