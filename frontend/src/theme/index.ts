/**Naive UI 主题配置

统一设计 Token:
- 主色: #1d9bf0 (Twitter Blue)
- 暗色基底: #0b0e14
- 间距: 4/8/12/16/24px 阶梯
*/

import { darkTheme, type GlobalThemeOverrides } from 'naive-ui'

export const themeOverrides: GlobalThemeOverrides = {
  common: {
    // 主色系
    primaryColor: '#1d9bf0',
    primaryColorHover: '#3baff5',
    primaryColorSuppl: '#3baff5',
    primaryColorPressed: '#1a8cd8',

    // 成功/警告/错误
    successColor: '#22c55e',
    warningColor: '#eab308',
    errorColor: '#ef4444',

    // 文字色
    textColor1: '#e2e8f0',
    textColor2: '#c8d0dc',
    textColor3: '#8892a6',
    textColorDisabled: '#4a5568',

    // 边框
    borderColor: '#1e2533',
    borderRadius: '10px',
    borderRadiusSmall: '6px',

    // 背景色
    popoverColor: '#1a202c',
    tableColor: '#1a202c',
    cardColor: '#1a202c',
    modalColor: '#1a202c',
    bodyColor: '#0b0e14',
    tagColor: '#1a202c',
    avatarColor: '#1a202c',
    inputColor: '#121720',
    codeColor: '#121720',
    tabColor: '#1a202c',
    actionColor: '#1a202c',
    tableHeaderColor: '#121720',
    hoverColor: '#1f2633',
    tableColorHover: '#1f2633',
    tableColorStriped: '#121720',
    pressedColor: '#151a24',
    buttonColor2: '#1f2633',
    buttonColor2Hover: '#2a3344',
    buttonColor2Pressed: '#1a202c',

    // 滚动条
    scrollbarColor: '#2a3344',
    scrollbarColorHover: '#3a4556',

    // 分隔线
    dividerColor: '#1e2533',

    // 字体
    fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, "Noto Sans SC", "PingFang SC", system-ui, sans-serif',
    fontFamilyMono: '"SF Mono", "Fira Code", "JetBrains Mono", monospace',
    fontWeight: '400',
    fontWeightStrong: '600',

    // 字号
    fontSize: '14px',
    fontSizeSmall: '12px',
    fontSizeMedium: '15px',
    fontSizeLarge: '18px',

    // 阴影
    boxShadow1: '0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)',
    boxShadow2: '0 4px 16px rgba(0,0,0,0.3)',

    // 占位符
    placeholderColor: '#4a5568',
  },
  Menu: {
    itemHeight: '40px',
    itemColorHover: '#1f2633',
    itemTextColor: '#8892a6',
    itemTextColorHover: '#e2e8f0',
    itemTextColorActive: '#1d9bf0',
    itemColorActive: 'rgba(29, 155, 240, 0.1)',
    dividerColor: '#1e2533',
  },
  Button: {
    heightMedium: '36px',
    heightSmall: '28px',
    textColorGhost: '#e2e8f0',
    textColorDisabled: '#4a5568',
  },
  Input: {
    placeholderColor: '#4a5568',
    textColor: '#e2e8f0',
  },
  Table: {
    textColor: '#e2e8f0',
  },
  Modal: {
    color: '#1a202c',
  },
  Tag: {},
}

export { darkTheme }
