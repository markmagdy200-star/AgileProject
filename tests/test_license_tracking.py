# Simple test script for license tracking and GUI display
from equipment_management import LicenseManager, SoftwareLicense
import tkinter as tk

# Test LicenseManager.track_licenses with dict and object entries
lm = LicenseManager()
# Add object-style license
lm.add_license(SoftwareLicense('L_OBJ', 'ObjectSoft', 4))
# Add dict-style legacy license
lm.licenses['L_DICT'] = {'name': 'LegacySoft', 'used_seats': 1, 'total_seats': 3}

tracked = lm.track_licenses()
assert 'L_OBJ' in tracked and 'L_DICT' in tracked, 'Both licenses must appear in tracked mapping'
assert tracked['L_OBJ']['name'] == 'ObjectSoft', 'Object license name mismatch'
assert tracked['L_DICT']['name'] == 'LegacySoft', 'Dict license name mismatch'

# Now sanity check GUI.refresh_license_info does not throw
from GUI import UniversityManagementGUI
from tkinter import messagebox
# suppress GUI popups
messagebox.showinfo = lambda *a, **k: None
messagebox.showwarning = lambda *a, **k: None
messagebox.showerror = lambda *a, **k: None

root = tk.Tk(); root.withdraw()
app = UniversityManagementGUI(root)
# Use our mixed license manager instance
app.license_manager = lm
# Call the refresh that previously failed
try:
    app.refresh_license_info()
    contents = app.license_display.get(1.0, 'end')
    assert 'L_OBJ' in contents and 'L_DICT' in contents, 'GUI display must contain both license IDs'
    print('TEST PASSED: License tracking and GUI display handle dict/object formats')
except Exception as e:
    print('TEST FAILED:', e)
finally:
    root.destroy()