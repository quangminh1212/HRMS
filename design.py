"""
HRMS Design System - Modern UI Components & Design Tokens
Tham khảo từ Material Design 3, Fluent Design, Ant Design
"""

class DesignTokens:
    """Design tokens cho consistency"""
    
    # Color System - Tham khảo Material Design 3
    COLORS = {
        # Primary Colors
        'primary': {
            10: '#21005D',
            20: '#381E72', 
            30: '#4F378B',
            40: '#6750A4',
            50: '#7F67BE',
            60: '#9A82DB',
            70: '#B69DF8',
            80: '#D0BCFF',
            90: '#EADDFF',
            95: '#F6EDFF',
            99: '#FFFBFE'
        },
        
        # Secondary Colors
        'secondary': {
            10: '#1D192B',
            20: '#332D41',
            30: '#4A4458',
            40: '#625B71',
            50: '#7A7289',
            60: '#958DA5',
            70: '#B0A7C0',
            80: '#CCC2DC',
            90: '#E8DEF8',
            95: '#F6EDFF',
            99: '#FFFBFE'
        },
        
        # Semantic Colors
        'success': '#4CAF50',
        'warning': '#FF9800', 
        'error': '#F44336',
        'info': '#2196F3',
        
        # Neutral Colors
        'neutral': {
            0: '#000000',
            10: '#1C1B1F',
            20: '#313033',
            30: '#484649',
            40: '#605D62',
            50: '#787579',
            60: '#939094',
            70: '#AEAAAE',
            80: '#CAC4D0',
            90: '#E6E0E9',
            95: '#F4EFF4',
            99: '#FFFBFE',
            100: '#FFFFFF'
        },
        
        # Surface Colors
        'surface': {
            'dim': '#DDD8E1',
            'bright': '#FFFBFE',
            'container_lowest': '#FFFFFF',
            'container_low': '#F7F2FA',
            'container': '#F3EDF7',
            'container_high': '#ECE6F0',
            'container_highest': '#E6E0E9'
        }
    }
    
    # Typography System
    TYPOGRAPHY = {
        'display_large': {
            'font_family': 'Inter',
            'font_size': '57px',
            'line_height': '64px',
            'font_weight': '400',
            'letter_spacing': '-0.25px'
        },
        'display_medium': {
            'font_family': 'Inter',
            'font_size': '45px', 
            'line_height': '52px',
            'font_weight': '400',
            'letter_spacing': '0px'
        },
        'display_small': {
            'font_family': 'Inter',
            'font_size': '36px',
            'line_height': '44px', 
            'font_weight': '400',
            'letter_spacing': '0px'
        },
        'headline_large': {
            'font_family': 'Inter',
            'font_size': '32px',
            'line_height': '40px',
            'font_weight': '400',
            'letter_spacing': '0px'
        },
        'headline_medium': {
            'font_family': 'Inter',
            'font_size': '28px',
            'line_height': '36px',
            'font_weight': '400', 
            'letter_spacing': '0px'
        },
        'headline_small': {
            'font_family': 'Inter',
            'font_size': '24px',
            'line_height': '32px',
            'font_weight': '400',
            'letter_spacing': '0px'
        },
        'title_large': {
            'font_family': 'Inter',
            'font_size': '22px',
            'line_height': '28px',
            'font_weight': '500',
            'letter_spacing': '0px'
        },
        'title_medium': {
            'font_family': 'Inter', 
            'font_size': '16px',
            'line_height': '24px',
            'font_weight': '500',
            'letter_spacing': '0.15px'
        },
        'title_small': {
            'font_family': 'Inter',
            'font_size': '14px',
            'line_height': '20px',
            'font_weight': '500',
            'letter_spacing': '0.1px'
        },
        'body_large': {
            'font_family': 'Inter',
            'font_size': '16px',
            'line_height': '24px',
            'font_weight': '400',
            'letter_spacing': '0.15px'
        },
        'body_medium': {
            'font_family': 'Inter',
            'font_size': '14px',
            'line_height': '20px',
            'font_weight': '400',
            'letter_spacing': '0.25px'
        },
        'body_small': {
            'font_family': 'Inter',
            'font_size': '12px',
            'line_height': '16px', 
            'font_weight': '400',
            'letter_spacing': '0.4px'
        },
        'label_large': {
            'font_family': 'Inter',
            'font_size': '14px',
            'line_height': '20px',
            'font_weight': '500',
            'letter_spacing': '0.1px'
        },
        'label_medium': {
            'font_family': 'Inter',
            'font_size': '12px',
            'line_height': '16px',
            'font_weight': '500',
            'letter_spacing': '0.5px'
        },
        'label_small': {
            'font_family': 'Inter',
            'font_size': '11px',
            'line_height': '16px',
            'font_weight': '500', 
            'letter_spacing': '0.5px'
        }
    }
    
    # Spacing System - 8px grid
    SPACING = {
        'xs': '4px',    # 0.5 unit
        'sm': '8px',    # 1 unit  
        'md': '16px',   # 2 units
        'lg': '24px',   # 3 units
        'xl': '32px',   # 4 units
        '2xl': '40px',  # 5 units
        '3xl': '48px',  # 6 units
        '4xl': '64px',  # 8 units
        '5xl': '80px',  # 10 units
        '6xl': '96px',  # 12 units
    }
    
    # Border Radius
    RADIUS = {
        'none': '0px',
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '20px',
        '2xl': '24px',
        '3xl': '28px',
        'full': '9999px'
    }
    
    # Shadows
    SHADOWS = {
        'level_1': '0px 1px 2px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)',
        'level_2': '0px 1px 2px rgba(0, 0, 0, 0.3), 0px 2px 6px 2px rgba(0, 0, 0, 0.15)',
        'level_3': '0px 4px 8px 3px rgba(0, 0, 0, 0.15), 0px 1px 3px rgba(0, 0, 0, 0.3)',
        'level_4': '0px 6px 10px 4px rgba(0, 0, 0, 0.15), 0px 2px 3px rgba(0, 0, 0, 0.3)',
        'level_5': '0px 8px 12px 6px rgba(0, 0, 0, 0.15), 0px 4px 4px rgba(0, 0, 0, 0.3)'
    }
    
    # Animation Duration
    DURATIONS = {
        'fast': '150ms',
        'normal': '300ms', 
        'slow': '500ms'
    }
    
    # Breakpoints
    BREAKPOINTS = {
        'mobile': '576px',
        'tablet': '768px', 
        'desktop': '1024px',
        'wide': '1440px'
    }

class UIComponents:
    """Modern UI Components System"""
    
    @staticmethod
    def get_base_css():
        """CSS cơ sở cho toàn bộ hệ thống"""
        return """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* CSS Reset và Base Styles */
        *, *::before, *::after {
            box-sizing: border-box;
        }
        
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 35%, #f093fb 100%);
            min-height: 100vh;
            color: #1C1B1F;
        }
        
        /* Container System */
        .main .block-container {
            padding: 1rem 2rem;
            max-width: 1200px;
        }
        
        /* Typography Classes */
        .display-large {
            font-size: 57px;
            line-height: 64px;
            font-weight: 400;
            letter-spacing: -0.25px;
        }
        
        .headline-medium {
            font-size: 28px;
            line-height: 36px; 
            font-weight: 400;
            letter-spacing: 0px;
        }
        
        .title-large {
            font-size: 22px;
            line-height: 28px;
            font-weight: 500;
            letter-spacing: 0px;
        }
        
        .body-large {
            font-size: 16px;
            line-height: 24px;
            font-weight: 400;
            letter-spacing: 0.15px;
        }
        
        .label-medium {
            font-size: 12px;
            line-height: 16px;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        /* Surface System - Glassmorphism Evolution */
        .surface-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.125);
            border-radius: 16px;
            box-shadow: 0px 4px 8px 3px rgba(0, 0, 0, 0.15), 0px 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .surface-container-high {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(24px) saturate(200%);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow: 0px 6px 10px 4px rgba(0, 0, 0, 0.15), 0px 2px 3px rgba(0, 0, 0, 0.3);
        }
        
        .surface-container-highest {
            background: rgba(255, 255, 255, 0.99);
            backdrop-filter: blur(28px) saturate(220%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            box-shadow: 0px 8px 12px 6px rgba(0, 0, 0, 0.15), 0px 4px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* Interactive States */
        .surface-container:hover {
            transform: translateY(-2px);
            box-shadow: 0px 8px 16px 6px rgba(0, 0, 0, 0.2), 0px 2px 6px rgba(0, 0, 0, 0.4);
            transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Header Hero Section */
        .hero-header {
            background: linear-gradient(135deg, 
                rgba(103, 80, 164, 0.95) 0%, 
                rgba(118, 75, 162, 0.9) 50%, 
                rgba(240, 147, 251, 0.85) 100%);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 28px;
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .hero-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            margin: 0;
            position: relative;
            z-index: 1;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: rgba(255, 255, 255, 0.9);
            margin: 1rem 0 0 0;
            position: relative;
            z-index: 1;
        }
        
        /* Card System */
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 1.5rem;
            transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #6750A4, #7F67BE, #9A82DB);
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0px 12px 24px 8px rgba(0, 0, 0, 0.2), 0px 4px 8px rgba(0, 0, 0, 0.4);
            background: rgba(255, 255, 255, 0.98);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        /* Icon System */
        .icon-container {
            width: 64px;
            height: 64px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1rem;
        }
        
        .icon-primary {
            background: linear-gradient(135deg, #6750A4, #7F67BE);
            color: white;
            box-shadow: 0 4px 12px rgba(103, 80, 164, 0.3);
        }
        
        .icon-success {
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
            color: white;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        }
        
        .icon-warning {
            background: linear-gradient(135deg, #FF9800, #FFB74D);
            color: white;
            box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
        }
        
        .icon-error {
            background: linear-gradient(135deg, #F44336, #EF5350);
            color: white;
            box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
        }
        
        /* Button System */
        .btn-primary {
            background: linear-gradient(135deg, #6750A4, #7F67BE);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 500;
            font-size: 14px;
            letter-spacing: 0.1px;
            cursor: pointer;
            transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(103, 80, 164, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(103, 80, 164, 0.4);
            background: linear-gradient(135deg, #5A4094, #7157B8);
        }
        
        /* Alert System */
        .alert {
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid transparent;
            position: relative;
            backdrop-filter: blur(10px);
        }
        
        .alert-warning {
            background: linear-gradient(135deg, rgba(255, 152, 0, 0.1), rgba(255, 183, 77, 0.15));
            border-color: rgba(255, 152, 0, 0.2);
            color: #E65100;
        }
        
        .alert-success {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(102, 187, 106, 0.15));
            border-color: rgba(76, 175, 80, 0.2);
            color: #1B5E20;
        }
        
        .alert-info {
            background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(100, 181, 246, 0.15));
            border-color: rgba(33, 150, 243, 0.2);
            color: #0D47A1;
        }
        
        .alert-error {
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(239, 83, 80, 0.15));
            border-color: rgba(244, 67, 54, 0.2);
            color: #B71C1C;
        }
        
        /* Navigation System */
        .nav-item {
            transition: all 200ms ease;
            border-radius: 12px;
            position: relative;
        }
        
        .nav-item:hover {
            background: rgba(103, 80, 164, 0.1);
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, rgba(103, 80, 164, 0.15), rgba(127, 103, 190, 0.1));
            border-left: 4px solid #6750A4;
        }
        
        /* Micro-animations */
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .animate-slide-up {
            animation: slideInUp 600ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        
        .animate-fade-scale {
            animation: fadeInScale 400ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        
        .animate-pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        /* Responsive System */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .metric-card {
                margin-bottom: 1rem;
            }
        }
        
        /* Streamlit Component Overrides */
        div[data-testid="metric-container"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, 
                rgba(255, 255, 255, 0.95) 0%, 
                rgba(255, 255, 255, 0.9) 100%) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #6750A4, #7F67BE) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(103, 80, 164, 0.3) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 16px rgba(103, 80, 164, 0.4) !important;
            background: linear-gradient(135deg, #5A4094, #7157B8) !important;
        }
        
        /* Chart Containers */
        .js-plotly-plot {
            background: rgba(255, 255, 255, 0.95) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            overflow: hidden !important;
            box-shadow: 0px 4px 8px 3px rgba(0, 0, 0, 0.15) !important;
        }
        </style>
        """
