import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from qfluentwidgets import (
    FluentWindow, NavigationItemPosition,
    SubtitleLabel, BodyLabel, CaptionLabel, StrongBodyLabel,
    PushButton, PrimaryPushButton, ToolButton,
    ComboBox, LineEdit, TextEdit, SpinBox, CheckBox, RadioButton,
    CardWidget, SimpleCardWidget,
    InfoBar, InfoBarPosition, MessageBox,
    FluentIcon as FIF, setTheme, Theme, isDarkTheme, themeColor,
    TransparentToolButton, TransparentPushButton,
    HyperlinkLabel, ProgressRing, ProgressBar,
    Dialog
)
from modes.popup_mode import PopupModeWidget
from modes.workflow_mode import WorkflowModeWidget


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WindowMatter - 弹窗创建工具")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # 设置窗口图标 - 使用绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            icon_path = os.path.join(base_dir, 'icon.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        
        self.popupModeWidget = PopupModeWidget(self)
        self.workflowModeWidget = WorkflowModeWidget(self)
        
        self.homeInterface = QWidget(self)
        self.homeInterface.setObjectName("homeInterface")
        self.popupInterface = QWidget(self)
        self.popupInterface.setObjectName("popupInterface")
        self.workflowInterface = QWidget(self)
        self.workflowInterface.setObjectName("workflowInterface")
        self.settingInterface = QWidget(self)
        self.settingInterface.setObjectName("settingInterface")
        
        self._initNavigation()
        self._initHomePage()
        self._initPopupPage()
        self._initWorkflowPage()
        self._initSettingPage()
        
    def _initNavigation(self):
        self.addSubInterface(
            self.homeInterface, 
            FIF.HOME, 
            "首页",
            NavigationItemPosition.TOP
        )
        self.addSubInterface(
            self.popupInterface,
            FIF.MESSAGE,
            "弹窗模式",
            NavigationItemPosition.TOP
        )
        self.addSubInterface(
            self.workflowInterface,
            FIF.SYNC,
            "工作流",
            NavigationItemPosition.TOP
        )
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "设置",
            NavigationItemPosition.BOTTOM
        )
        
    def _initHomePage(self):
        layout = QVBoxLayout(self.homeInterface)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = SubtitleLabel("欢迎使用 WindowMatter", self.homeInterface)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = BodyLabel("一个强大的弹窗创建工具，支持 Win11 风格设计", self.homeInterface)
        desc.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(desc)
        
        layout.addSpacing(30)
        
        card1 = self._createFeatureCard(
            FIF.MESSAGE,
            "弹窗模式",
            "快速创建各种类型的弹窗，支持警告、提示、错误、疑问等图标，支持输入框、单选、多选",
            self.homeInterface
        )
        layout.addWidget(card1)
        
        card2 = self._createFeatureCard(
            FIF.SYNC,
            "工作流",
            "创建多个弹窗的序列，实现自动化弹窗流程",
            self.homeInterface
        )
        layout.addWidget(card2)
        
        card3 = self._createFeatureCard(
            FIF.SAVE,
            "保存配置",
            "支持保存为 .winmt 格式，可独立运行",
            self.homeInterface
        )
        layout.addWidget(card3)
        
        card4 = self._createFeatureCard(
            FIF.PALETTE,
            "多种样式",
            "支持 WinUI、MessageBox、ContentDialog 三种风格，支持浅色/深色主题",
            self.homeInterface
        )
        layout.addWidget(card4)
        
        layout.addStretch()
        
    def _createFeatureCard(self, icon, title, desc, parent):
        card = CardWidget(parent)
        card.setFixedHeight(120)
        
        hLayout = QHBoxLayout(card)
        hLayout.setContentsMargins(20, 15, 20, 15)
        hLayout.setSpacing(15)
        
        iconWidget = QLabel(card)
        iconWidget.setFixedSize(56, 56)
        iconWidget.setAlignment(Qt.AlignCenter)
        iconWidget.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 120, 212, 0.1);
                border-radius: 12px;
                font-size: 24px;
            }
        """)
        iconWidget.setText("📦")
        hLayout.addWidget(iconWidget)
        
        vLayout = QVBoxLayout()
        vLayout.setSpacing(6)
        
        titleLabel = StrongBodyLabel(title, card)
        titleLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        vLayout.addWidget(titleLabel)
        
        descLabel = CaptionLabel(desc, card)
        descLabel.setWordWrap(True)
        descLabel.setStyleSheet("font-size: 12px; color: #888;")
        vLayout.addWidget(descLabel)
        
        hLayout.addLayout(vLayout, 1)
        hLayout.addStretch()
        
        return card
        
    def _initPopupPage(self):
        layout = QVBoxLayout(self.popupInterface)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.popupModeWidget)
        
    def _initWorkflowPage(self):
        layout = QVBoxLayout(self.workflowInterface)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.workflowModeWidget)
        
    def _initSettingPage(self):
        layout = QVBoxLayout(self.settingInterface)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        layout.addWidget(SubtitleLabel("设置", self.settingInterface))
        layout.addSpacing(20)
        
        themeCard = CardWidget(self.settingInterface)
        themeLayout = QHBoxLayout(themeCard)
        themeLayout.setContentsMargins(20, 15, 20, 15)
        themeLayout.addWidget(BodyLabel("主题:", themeCard))
        self.themeCombo = ComboBox(themeCard)
        self.themeCombo.addItems(["跟随系统", "浅色", "深色"])
        self.themeCombo.currentIndexChanged.connect(self._onThemeChanged)
        themeLayout.addWidget(self.themeCombo)
        themeLayout.addStretch()
        layout.addWidget(themeCard)
        
        aboutCard = CardWidget(self.settingInterface)
        aboutLayout = QVBoxLayout(aboutCard)
        aboutLayout.setContentsMargins(20, 15, 20, 15)
        aboutLayout.addWidget(StrongBodyLabel("关于 WindowMatter", aboutCard))
        aboutLayout.addWidget(BodyLabel("版本: 1.0.0", aboutCard))
        aboutLayout.addWidget(BodyLabel("一个强大的弹窗创建工具", aboutCard))
        layout.addWidget(aboutCard)
        
        layout.addStretch()
        
    def _onThemeChanged(self, index):
        themes = [Theme.AUTO, Theme.LIGHT, Theme.DARK]
        if index < len(themes):
            setTheme(themes[index])
