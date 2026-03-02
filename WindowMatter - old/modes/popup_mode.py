import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QSizePolicy, QSpacerItem,
    QButtonGroup, QFileDialog, QMessageBox as QtMsgBox,
    QDialog, QLineEdit, QRadioButton, QCheckBox, QPushButton
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon
from qfluentwidgets import (
    SubtitleLabel, BodyLabel, CaptionLabel, StrongBodyLabel,
    PushButton as FluentPushButton, PrimaryPushButton, ComboBox, LineEdit as FluentLineEdit, TextEdit,
    SpinBox, CheckBox as FluentCheckBox, RadioButton as FluentRadioButton, SwitchButton,
    CardWidget, SimpleCardWidget,
    FluentIcon as FIF, isDarkTheme, InfoBar, InfoBarPosition,
    MessageBox, Dialog, setTheme, Theme,
    ListWidget, ListItemDelegate
)


class IconSelector(CardWidget):
    iconChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectedIcon = "info"
        self._initUI()
        
    def _initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        layout.addWidget(StrongBodyLabel("图标类型", self))
        
        gridLayout = QGridLayout()
        gridLayout.setSpacing(8)
        
        self.icons = [
            ("warning", "⚠ 警告", "#ff8c00"),
            ("info", "ℹ 提示", "#0078d4"),
            ("error", "✖ 错误", "#d13438"),
            ("question", "? 疑问", "#0078d4"),
            ("success", "✓ 成功", "#107c10"),
            ("none", "○ 无图标", "#666666"),
        ]
        
        self.iconButtons = []
        for i, (iconId, iconText, color) in enumerate(self.icons):
            btn = FluentPushButton(iconText, self)
            btn.setCheckable(True)
            btn.setFixedHeight(40)
            btn.setStyleSheet(f"""
                PushButton {{
                    border: 2px solid transparent;
                    border-radius: 6px;
                    padding: 5px;
                }}
                PushButton:checked {{
                    border: 2px solid {color};
                    background-color: {color}20;
                }}
            """)
            btn.clicked.connect(lambda checked, id=iconId: self._selectIcon(id))
            self.iconButtons.append((iconId, btn))
            row = i // 2
            col = i % 2
            gridLayout.addWidget(btn, row, col)
            
        layout.addLayout(gridLayout)
        self._selectIcon("info")
        
    def _selectIcon(self, iconId):
        self.selectedIcon = iconId
        for iconId_, btn in self.iconButtons:
            btn.setChecked(iconId_ == iconId)
        self.iconChanged.emit(iconId)
            
    def getSelectedIcon(self):
        return self.selectedIcon
    
    def setSelectedIcon(self, iconId):
        if iconId in [i[0] for i in self.icons]:
            self._selectIcon(iconId)


class ButtonSelector(CardWidget):
    buttonsChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectedButtons = "ok"
        self._initUI()
        
    def _initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        layout.addWidget(StrongBodyLabel("按钮组合", self))
        
        self.buttonPresets = [
            ("ok", "确定"),
            ("ok_cancel", "确定 / 取消"),
            ("yes_no", "是 / 否"),
            ("yes_no_cancel", "是 / 否 / 取消"),
            ("retry_cancel", "重试 / 取消"),
            ("abort_retry_ignore", "中止 / 重试 / 忽略"),
        ]
        
        self.presetButtons = []
        for buttonId, buttonText in self.buttonPresets:
            btn = FluentPushButton(buttonText, self)
            btn.setCheckable(True)
            btn.setFixedHeight(36)
            btn.clicked.connect(lambda checked, id=buttonId: self._selectPreset(id))
            self.presetButtons.append((buttonId, btn))
            layout.addWidget(btn)
            
        self._selectPreset("ok")
        
    def _selectPreset(self, presetId):
        self.selectedButtons = presetId
        for presetId_, btn in self.presetButtons:
            btn.setChecked(presetId_ == presetId)
        self.buttonsChanged.emit(presetId)
            
    def getSelectedButtons(self):
        return self.selectedButtons
    
    def setSelectedButtons(self, presetId):
        if presetId in [p[0] for p in self.buttonPresets]:
            self._selectPreset(presetId)


class InputOptionsCard(CardWidget):
    optionsChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()
        
    def _initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        layout.addWidget(StrongBodyLabel("输入选项", self))
        
        self.hasInputCheck = FluentCheckBox("显示输入框", self)
        self.hasInputCheck.stateChanged.connect(self.optionsChanged.emit)
        layout.addWidget(self.hasInputCheck)
        
        self.inputPlaceholderEdit = FluentLineEdit(self)
        self.inputPlaceholderEdit.setPlaceholderText("输入框提示文字")
        self.inputPlaceholderEdit.setText("请输入内容...")
        layout.addWidget(self.inputPlaceholderEdit)
        
        self.hasRadioCheck = FluentCheckBox("显示单选按钮", self)
        self.hasRadioCheck.stateChanged.connect(self._onRadioCheckChanged)
        layout.addWidget(self.hasRadioCheck)
        
        self.radioOptionsEdit = TextEdit(self)
        self.radioOptionsEdit.setPlaceholderText("每行一个选项")
        self.radioOptionsEdit.setText("选项1\n选项2\n选项3")
        self.radioOptionsEdit.setFixedHeight(60)
        layout.addWidget(self.radioOptionsEdit)
        
        self.hasCheckCheck = FluentCheckBox("显示复选框", self)
        self.hasCheckCheck.stateChanged.connect(self._onCheckCheckChanged)
        layout.addWidget(self.hasCheckCheck)
        
        self.checkOptionsEdit = TextEdit(self)
        self.checkOptionsEdit.setPlaceholderText("每行一个选项")
        self.checkOptionsEdit.setText("选项A\n选项B\n选项C")
        self.checkOptionsEdit.setFixedHeight(60)
        layout.addWidget(self.checkOptionsEdit)
        
        self._onRadioCheckChanged()
        self._onCheckCheckChanged()
        
    def _onRadioCheckChanged(self):
        self.radioOptionsEdit.setEnabled(self.hasRadioCheck.isChecked())
        self.optionsChanged.emit()
        
    def _onCheckCheckChanged(self):
        self.checkOptionsEdit.setEnabled(self.hasCheckCheck.isChecked())
        self.optionsChanged.emit()
        
    def getOptions(self):
        return {
            "hasInput": self.hasInputCheck.isChecked(),
            "inputPlaceholder": self.inputPlaceholderEdit.text(),
            "hasRadio": self.hasRadioCheck.isChecked(),
            "radioOptions": self.radioOptionsEdit.toPlainText().strip().split("\n") if self.hasRadioCheck.isChecked() else [],
            "hasCheck": self.hasCheckCheck.isChecked(),
            "checkOptions": self.checkOptionsEdit.toPlainText().strip().split("\n") if self.hasCheckCheck.isChecked() else []
        }
    
    def setOptions(self, options):
        self.hasInputCheck.setChecked(options.get("hasInput", False))
        self.inputPlaceholderEdit.setText(options.get("inputPlaceholder", "请输入内容..."))
        self.hasRadioCheck.setChecked(options.get("hasRadio", False))
        self.radioOptionsEdit.setText("\n".join(options.get("radioOptions", ["选项1", "选项2", "选项3"])))
        self.hasCheckCheck.setChecked(options.get("hasCheck", False))
        self.checkOptionsEdit.setText("\n".join(options.get("checkOptions", ["选项A", "选项B", "选项C"])))


class PopupModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentConfig = {}
        self._initUI()
        
    def _initUI(self):
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)
        
        leftPanel = self._createLeftPanel()
        mainLayout.addWidget(leftPanel, 3)
        
        rightPanel = self._createRightPanel()
        mainLayout.addWidget(rightPanel, 1)
        
    def _createLeftPanel(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        titleCard = CardWidget()
        titleLayout = QHBoxLayout(titleCard)
        titleLayout.setContentsMargins(20, 15, 20, 15)
        titleLayout.addWidget(SubtitleLabel("弹窗模式"))
        titleLayout.addStretch()
        layout.addWidget(titleCard)
        
        settingsCard = CardWidget()
        settingsLayout = QVBoxLayout(settingsCard)
        settingsLayout.setContentsMargins(20, 20, 20, 20)
        settingsLayout.setSpacing(15)
        
        settingsLayout.addWidget(StrongBodyLabel("基本设置"))
        
        titleRow = QHBoxLayout()
        titleRow.addWidget(BodyLabel("标题:"))
        self.titleEdit = FluentLineEdit()
        self.titleEdit.setPlaceholderText("输入弹窗标题")
        self.titleEdit.setText("提示")
        titleRow.addWidget(self.titleEdit, 1)
        settingsLayout.addLayout(titleRow)
        
        settingsLayout.addWidget(BodyLabel("内容:"))
        self.contentEdit = TextEdit()
        self.contentEdit.setPlaceholderText("输入弹窗内容")
        self.contentEdit.setText("这是一个弹窗示例")
        self.contentEdit.setFixedHeight(100)
        settingsLayout.addWidget(self.contentEdit)
        
        settingsLayout.addSpacing(10)
        settingsLayout.addWidget(StrongBodyLabel("样式设置"))
        
        styleRow = QHBoxLayout()
        styleRow.addWidget(BodyLabel("弹窗样式:"))
        self.styleCombo = ComboBox()
        self.styleCombo.addItems(["WinUI 风格", "MessageBox 风格", "ContentDialog 风格"])
        styleRow.addWidget(self.styleCombo)
        styleRow.addStretch()
        settingsLayout.addLayout(styleRow)
        
        themeRow = QHBoxLayout()
        themeRow.addWidget(BodyLabel("主题:"))
        self.themeCombo = ComboBox()
        self.themeCombo.addItems(["跟随系统", "浅色", "深色"])
        themeRow.addWidget(self.themeCombo)
        themeRow.addStretch()
        settingsLayout.addLayout(themeRow)
        
        layout.addWidget(settingsCard)
        
        self.inputOptionsCard = InputOptionsCard()
        layout.addWidget(self.inputOptionsCard)
        
        actionCard = CardWidget()
        actionLayout = QVBoxLayout(actionCard)
        actionLayout.setContentsMargins(20, 20, 20, 20)
        actionLayout.setSpacing(10)
        
        actionLayout.addWidget(StrongBodyLabel("操作"))
        
        btnRow = QHBoxLayout()
        
        previewBtn = PrimaryPushButton("预览弹窗")
        previewBtn.setIcon(FIF.PLAY)
        previewBtn.clicked.connect(self._showPreview)
        btnRow.addWidget(previewBtn)
        
        btnRow.addSpacing(10)
        
        saveBtn = FluentPushButton("保存配置")
        saveBtn.setIcon(FIF.SAVE)
        saveBtn.clicked.connect(self._saveConfig)
        btnRow.addWidget(saveBtn)
        
        loadBtn = FluentPushButton("加载配置")
        loadBtn.setIcon(FIF.FOLDER)
        loadBtn.clicked.connect(self._loadConfig)
        btnRow.addWidget(loadBtn)
        
        exportBtn = FluentPushButton("导出可执行文件")
        exportBtn.setIcon(FIF.SHARE)
        exportBtn.clicked.connect(self._exportExecutable)
        btnRow.addWidget(exportBtn)
        
        btnRow.addStretch()
        actionLayout.addLayout(btnRow)
        
        layout.addWidget(actionCard)
        layout.addStretch()
        
        scroll.setWidget(panel)
        return scroll
        
    def _createRightPanel(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setFixedWidth(250)
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        self.iconSelector = IconSelector()
        layout.addWidget(self.iconSelector)
        
        self.buttonSelector = ButtonSelector()
        layout.addWidget(self.buttonSelector)
        
        layout.addStretch()
        
        scroll.setWidget(panel)
        return scroll
        
    def _getConfig(self):
        return {
            "title": self.titleEdit.text(),
            "content": self.contentEdit.toPlainText(),
            "icon": self.iconSelector.getSelectedIcon(),
            "buttons": self.buttonSelector.getSelectedButtons(),
            "style": self.styleCombo.currentIndex(),
            "theme": self.themeCombo.currentIndex(),
            "inputOptions": self.inputOptionsCard.getOptions()
        }
    
    def _applyConfig(self, config):
        self.titleEdit.setText(config.get("title", "提示"))
        self.contentEdit.setText(config.get("content", "这是一个弹窗示例"))
        self.iconSelector.setSelectedIcon(config.get("icon", "info"))
        self.buttonSelector.setSelectedButtons(config.get("buttons", "ok"))
        self.styleCombo.setCurrentIndex(config.get("style", 0))
        self.themeCombo.setCurrentIndex(config.get("theme", 0))
        self.inputOptionsCard.setOptions(config.get("inputOptions", {}))
        
    def _showPreview(self):
        config = self._getConfig()
        title = config["title"] or "提示"
        content = config["content"] or "这是一个弹窗示例"
        iconType = config["icon"]
        buttonPreset = config["buttons"]
        styleIndex = config["style"]
        themeIndex = config["theme"]
        inputOptions = config["inputOptions"]
        
        themes = [Theme.AUTO, Theme.LIGHT, Theme.DARK]
        if themeIndex < len(themes):
            setTheme(themes[themeIndex])
        
        if styleIndex == 0:
            self._showWinUIDialog(title, content, iconType, buttonPreset, inputOptions)
        elif styleIndex == 1:
            self._showMessageBoxDialog(title, content, iconType, buttonPreset, inputOptions)
        else:
            self._showContentDialogDialog(title, content, iconType, buttonPreset, inputOptions)
    
    def _getIconEmoji(self, iconType):
        """获取图标对应的表情符号"""
        icon_map = {
            "warning": "⚠️",
            "info": "ℹ️",
            "error": "❌",
            "question": "❓",
            "success": "✅",
            "none": ""
        }
        return icon_map.get(iconType, "ℹ️")
    
    def _showWinUIDialog(self, title, content, iconType, buttonPreset, inputOptions):
        """显示WinUI风格对话框 - 使用自定义QDialog来支持图标"""
        dialog = QDialog(self.window())
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(400)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 设置窗口图标
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'icon.ico')
        if os.path.exists(icon_path):
            dialog.setWindowIcon(QIcon(icon_path))
        else:
            icon_path = os.path.join(base_dir, 'icon.png')
            if os.path.exists(icon_path):
                dialog.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标和内容区域
        headerLayout = QHBoxLayout()
        
        iconEmoji = self._getIconEmoji(iconType)
        if iconEmoji:
            iconLabel = QLabel(iconEmoji)
            iconLabel.setStyleSheet("font-size: 48px;")
            headerLayout.addWidget(iconLabel)
        
        contentLabel = QLabel(content)
        contentLabel.setWordWrap(True)
        contentLabel.setStyleSheet("font-size: 14px;")
        headerLayout.addWidget(contentLabel, 1)
        layout.addLayout(headerLayout)
        
        # 输入选项
        inputWidgets = []
        
        if inputOptions.get("hasInput", False):
            inputEdit = QLineEdit()
            inputEdit.setPlaceholderText(inputOptions.get("inputPlaceholder", "请输入内容..."))
            layout.addWidget(inputEdit)
            inputWidgets.append(("input", inputEdit))
            
        if inputOptions.get("hasRadio", False) and inputOptions.get("radioOptions"):
            radioGroup = QButtonGroup(dialog)
            for i, option in enumerate(inputOptions["radioOptions"]):
                if option.strip():
                    radio = QRadioButton(option.strip())
                    radioGroup.addButton(radio, i)
                    layout.addWidget(radio)
                    if i == 0:
                        radio.setChecked(True)
            inputWidgets.append(("radio", radioGroup))
            
        if inputOptions.get("hasCheck", False) and inputOptions.get("checkOptions"):
            checkBoxes = []
            for option in inputOptions["checkOptions"]:
                if option.strip():
                    check = QCheckBox(option.strip())
                    layout.addWidget(check)
                    checkBoxes.append(check)
            inputWidgets.append(("check", checkBoxes))
        
        # 按钮
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        
        if buttonPreset == "ok":
            okBtn = QPushButton("确定")
            okBtn.clicked.connect(dialog.accept)
            btnLayout.addWidget(okBtn)
        elif buttonPreset == "ok_cancel":
            okBtn = QPushButton("确定")
            okBtn.clicked.connect(dialog.accept)
            btnLayout.addWidget(okBtn)
            cancelBtn = QPushButton("取消")
            cancelBtn.clicked.connect(dialog.reject)
            btnLayout.addWidget(cancelBtn)
        elif buttonPreset == "yes_no":
            yesBtn = QPushButton("是")
            yesBtn.clicked.connect(dialog.accept)
            btnLayout.addWidget(yesBtn)
            noBtn = QPushButton("否")
            noBtn.clicked.connect(dialog.reject)
            btnLayout.addWidget(noBtn)
        elif buttonPreset == "retry_cancel":
            retryBtn = QPushButton("重试")
            retryBtn.clicked.connect(dialog.accept)
            btnLayout.addWidget(retryBtn)
            cancelBtn = QPushButton("取消")
            cancelBtn.clicked.connect(dialog.reject)
            btnLayout.addWidget(cancelBtn)
        else:
            okBtn = QPushButton("确定")
            okBtn.clicked.connect(dialog.accept)
            btnLayout.addWidget(okBtn)
            cancelBtn = QPushButton("取消")
            cancelBtn.clicked.connect(dialog.reject)
            btnLayout.addWidget(cancelBtn)
        
        layout.addLayout(btnLayout)
        
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            InfoBar.success(
                title="用户选择",
                content="用户点击了确认按钮",
                parent=self.window(),
                duration=2000
            )
        else:
            InfoBar.warning(
                title="用户选择", 
                content="用户点击了取消/关闭按钮",
                parent=self.window(),
                duration=2000
            )
            
    def _showMessageBoxDialog(self, title, content, iconType, buttonPreset, inputOptions):
        """显示MessageBox风格对话框"""
        # 使用 Qt 的 QMessageBox 来显示带图标的弹窗
        box = QtMsgBox(self.window())
        box.setWindowTitle(title)
        box.setText(content)
        
        # 设置图标
        icon_map = {
            "warning": QtMsgBox.Warning,
            "info": QtMsgBox.Information,
            "error": QtMsgBox.Critical,
            "question": QtMsgBox.Question,
            "success": QtMsgBox.Information,
            "none": QtMsgBox.NoIcon
        }
        box.setIcon(icon_map.get(iconType, QtMsgBox.Information))
        
        # 设置按钮
        if buttonPreset == "ok":
            box.setStandardButtons(QtMsgBox.Ok)
        elif buttonPreset == "ok_cancel":
            box.setStandardButtons(QtMsgBox.Ok | QtMsgBox.Cancel)
        elif buttonPreset == "yes_no":
            box.setStandardButtons(QtMsgBox.Yes | QtMsgBox.No)
        elif buttonPreset == "yes_no_cancel":
            box.setStandardButtons(QtMsgBox.Yes | QtMsgBox.No | QtMsgBox.Cancel)
        else:
            box.setStandardButtons(QtMsgBox.Ok | QtMsgBox.Cancel)
        
        # 设置窗口图标
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'icon.ico')
        if os.path.exists(icon_path):
            box.setWindowIcon(QIcon(icon_path))
        else:
            icon_path = os.path.join(base_dir, 'icon.png')
            if os.path.exists(icon_path):
                box.setWindowIcon(QIcon(icon_path))
        
        result = box.exec()
        
        if result in [QtMsgBox.Ok, QtMsgBox.Yes]:
            InfoBar.success(
                title="弹窗已关闭",
                content="用户点击了确定/是按钮",
                parent=self.window(),
                duration=2000
            )
        else:
            InfoBar.warning(
                title="弹窗已关闭",
                content="用户点击了取消/否按钮",
                parent=self.window(),
                duration=2000
            )
            
    def _showContentDialogDialog(self, title, content, iconType, buttonPreset, inputOptions):
        """显示ContentDialog风格对话框"""
        dialog = QDialog(self.window())
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(400)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 设置窗口图标
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'icon.ico')
        if os.path.exists(icon_path):
            dialog.setWindowIcon(QIcon(icon_path))
        else:
            icon_path = os.path.join(base_dir, 'icon.png')
            if os.path.exists(icon_path):
                dialog.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标和内容
        headerLayout = QHBoxLayout()
        
        iconEmoji = self._getIconEmoji(iconType)
        if iconEmoji:
            iconLabel = QLabel(iconEmoji)
            iconLabel.setStyleSheet("font-size: 48px;")
            headerLayout.addWidget(iconLabel)
        
        contentLabel = QLabel(content)
        contentLabel.setWordWrap(True)
        contentLabel.setStyleSheet("font-size: 14px;")
        headerLayout.addWidget(contentLabel, 1)
        layout.addLayout(headerLayout)
        
        # 按钮
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        
        okBtn = QPushButton("确定")
        okBtn.clicked.connect(dialog.accept)
        btnLayout.addWidget(okBtn)
        
        layout.addLayout(btnLayout)
        
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            InfoBar.success(
                title="用户选择",
                content="用户点击了确定按钮",
                parent=self.window(),
                duration=2000
            )
    
    def _saveConfig(self):
        config = self._getConfig()
        
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "保存配置",
            "",
            "WindowMatter 配置文件 (*.winmt)"
        )
        
        if filePath:
            if not filePath.endswith(".winmt"):
                filePath += ".winmt"
            try:
                with open(filePath, "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                InfoBar.success(
                    title="保存成功",
                    content=f"配置已保存到: {filePath}",
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
    
    def _loadConfig(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "加载配置",
            "",
            "WindowMatter 配置文件 (*.winmt)"
        )
        
        if filePath:
            try:
                with open(filePath, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self._applyConfig(config)
                InfoBar.success(
                    title="加载成功",
                    content=f"配置已从 {filePath} 加载",
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
    
    def _exportExecutable(self):
        config = self._getConfig()
        
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "导出可执行文件",
            "popup.py",
            "Python 文件 (*.py)"
        )
        
        if filePath:
            try:
                script_content = self._generateExecutableScript(config)
                with open(filePath, "w", encoding="utf-8") as f:
                    f.write(script_content)
                InfoBar.success(
                    title="导出成功",
                    content=f"可执行脚本已保存到: {filePath}",
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
    
    def _generateExecutableScript(self, config):
        script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WindowMatter 自动生成的弹窗脚本

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QCheckBox, QButtonGroup, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PopupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(''' + repr(config["title"]) + ''')
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标和标题
        headerLayout = QHBoxLayout()
        iconLabel = QLabel()
        
        icon_map = {
            "warning": "⚠️",
            "info": "ℹ️",
            "error": "❌",
            "question": "❓",
            "success": "✅",
            "none": ""
        }
        icon_text = icon_map.get(''' + repr(config["icon"]) + ''', "ℹ️")
        if icon_text:
            iconLabel.setText(icon_text)
            iconLabel.setStyleSheet("font-size: 32px;")
            headerLayout.addWidget(iconLabel)
        
        contentLabel = QLabel(''' + repr(config["content"]) + ''')
        contentLabel.setWordWrap(True)
        contentLabel.setStyleSheet("font-size: 14px;")
        headerLayout.addWidget(contentLabel, 1)
        layout.addLayout(headerLayout)
        
        # 输入选项
'''
        
        inputOptions = config.get("inputOptions", {})
        
        if inputOptions.get("hasInput", False):
            script += '''
        self.inputEdit = QLineEdit()
        self.inputEdit.setPlaceholderText(''' + repr(inputOptions.get("inputPlaceholder", "请输入内容...")) + ''')
        layout.addWidget(self.inputEdit)
'''
        
        if inputOptions.get("hasRadio", False) and inputOptions.get("radioOptions"):
            script += '''
        self.radioGroup = QButtonGroup(self)
'''
            for i, option in enumerate(inputOptions["radioOptions"]):
                if option.strip():
                    script += '''
        radio''' + str(i) + ''' = QRadioButton(''' + repr(option.strip()) + ''')
        self.radioGroup.addButton(radio''' + str(i) + ''', ''' + str(i) + ''')
        layout.addWidget(radio''' + str(i) + ''')
'''
            script += '''
        if self.radioGroup.buttons():
            self.radioGroup.buttons()[0].setChecked(True)
'''
        
        if inputOptions.get("hasCheck", False) and inputOptions.get("checkOptions"):
            script += '''
        self.checkBoxes = []
'''
            for i, option in enumerate(inputOptions["checkOptions"]):
                if option.strip():
                    script += '''
        check''' + str(i) + ''' = QCheckBox(''' + repr(option.strip()) + ''')
        self.checkBoxes.append(check''' + str(i) + ''')
        layout.addWidget(check''' + str(i) + ''')
'''
        
        script += '''
        # 按钮
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
'''
        
        buttonPreset = config["buttons"]
        if buttonPreset == "ok":
            script += '''
        okBtn = QPushButton("确定")
        okBtn.clicked.connect(self.accept)
        btnLayout.addWidget(okBtn)
'''
        elif buttonPreset in ["ok_cancel", "yes_no", "retry_cancel"]:
            btn1 = {"ok_cancel": "确定", "yes_no": "是", "retry_cancel": "重试"}[buttonPreset]
            btn2 = {"ok_cancel": "取消", "yes_no": "否", "retry_cancel": "取消"}[buttonPreset]
            script += '''
        btn1 = QPushButton("''' + btn1 + '''")
        btn1.clicked.connect(self.accept)
        btnLayout.addWidget(btn1)
        
        btn2 = QPushButton("''' + btn2 + '''")
        btn2.clicked.connect(self.reject)
        btnLayout.addWidget(btn2)
'''
        else:
            script += '''
        okBtn = QPushButton("确定")
        okBtn.clicked.connect(self.accept)
        btnLayout.addWidget(okBtn)
        
        cancelBtn = QPushButton("取消")
        cancelBtn.clicked.connect(self.reject)
        btnLayout.addWidget(cancelBtn)
'''
        
        script += '''
        layout.addLayout(btnLayout)
    
    def getResult(self):
        result = {}
'''
        
        if inputOptions.get("hasInput", False):
            script += '''
        result["input"] = self.inputEdit.text()
'''
        
        if inputOptions.get("hasRadio", False):
            script += '''
        result["radio"] = self.radioGroup.checkedId() if self.radioGroup.checkedButton() else -1
'''
        
        if inputOptions.get("hasCheck", False):
            script += '''
        result["checks"] = [cb.isChecked() for cb in self.checkBoxes]
'''
        
        script += '''
        return result

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 10))
    
    dialog = PopupDialog()
    result = dialog.exec()
    
    if result == QDialog.Accepted:
        print("用户点击了确定")
        print("结果:", dialog.getResult())
    else:
        print("用户点击了取消")
    
    return result

if __name__ == '__main__':
    sys.exit(main())
'''
        
        return script
