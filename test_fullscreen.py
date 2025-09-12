"""
Test script để verify fullscreen functionality của HRMS Desktop
"""

import customtkinter as ctk
import tkinter as tk

def test_fullscreen():
    """Test fullscreen capabilities"""
    print("🔧 Testing fullscreen support...")
    
    # Create simple test window
    root = ctk.CTk()
    root.title("🧪 HRMS Fullscreen Test")
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    print(f"📺 Screen resolution: {screen_width}x{screen_height}")
    
    # Set 90% screen size
    start_width = int(screen_width * 0.9)
    start_height = int(screen_height * 0.9)
    
    root.geometry(f"{start_width}x{start_height}")
    print(f"🖼️  Window size: {start_width}x{start_height}")
    
    # Fullscreen state
    is_fullscreen = [False]
    
    def toggle_fullscreen(event=None):
        is_fullscreen[0] = not is_fullscreen[0]
        if is_fullscreen[0]:
            root.attributes("-fullscreen", True)
            status_label.configure(text="✅ FULLSCREEN MODE - Press ESC to exit")
            print("🔳 Entered fullscreen mode")
        else:
            root.attributes("-fullscreen", False)
            status_label.configure(text="🔲 WINDOWED MODE - Press F11 for fullscreen")
            print("🪟 Returned to windowed mode")
    
    def exit_fullscreen(event=None):
        if is_fullscreen[0]:
            is_fullscreen[0] = False
            root.attributes("-fullscreen", False)
            status_label.configure(text="🔲 WINDOWED MODE - Press F11 for fullscreen")
            print("🚪 Exited fullscreen mode")
    
    # Bind keys
    root.bind('<F11>', toggle_fullscreen)
    root.bind('<Escape>', exit_fullscreen)
    
    # UI
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    title = ctk.CTkLabel(main_frame, text="🧪 HRMS Desktop Fullscreen Test", 
                        font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=30)
    
    status_label = ctk.CTkLabel(main_frame, text="🔲 WINDOWED MODE - Press F11 for fullscreen",
                               font=ctk.CTkFont(size=16))
    status_label.pack(pady=20)
    
    # Buttons
    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.pack(pady=30)
    
    fullscreen_btn = ctk.CTkButton(btn_frame, text="🔳 Toggle Fullscreen (F11)", 
                                  command=toggle_fullscreen, width=200)
    fullscreen_btn.pack(side="left", padx=10)
    
    exit_btn = ctk.CTkButton(btn_frame, text="🚪 Exit Fullscreen (ESC)", 
                            command=exit_fullscreen, width=200)
    exit_btn.pack(side="left", padx=10)
    
    quit_btn = ctk.CTkButton(btn_frame, text="❌ Quit Test", 
                            command=root.destroy, width=150)
    quit_btn.pack(side="left", padx=10)
    
    # Info
    info_text = """
    ⌨️ KEYBOARD SHORTCUTS:
    • F11: Toggle fullscreen
    • ESC: Exit fullscreen
    • Click buttons above to test
    
    📋 FEATURES TESTING:
    ✅ Screen size detection
    ✅ 90% initial size  
    ✅ Fullscreen toggle
    ✅ Keyboard shortcuts
    ✅ Responsive layout
    """
    
    info_label = ctk.CTkLabel(main_frame, text=info_text, 
                             font=ctk.CTkFont(size=12), justify="left")
    info_label.pack(pady=30)
    
    print("✅ Test window ready!")
    print("📋 Instructions:")
    print("   • Press F11 to test fullscreen")
    print("   • Press ESC to exit fullscreen")  
    print("   • Close window to end test")
    
    # Center and show
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
    
    print("🏁 Fullscreen test completed!")

if __name__ == "__main__":
    try:
        test_fullscreen()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        input("Press Enter to close...")
