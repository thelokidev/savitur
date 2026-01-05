/**
 * Quick Frontend Code Verification Script
 * Run this in browser console to check if the fix is loaded
 */

// Check localStorage
console.log('=== LOCALSTORAGE CHECK ===');
console.log('Current localStorage:', localStorage.getItem('birth-details-storage'));
console.log('');

// Clear localStorage
localStorage.clear();
console.log('✓ localStorage cleared');
console.log('');

// Instructions
console.log('=== NEXT STEPS ===');
console.log('1. Refresh this page (Ctrl+Shift+R)');
console.log('2. Open this console again');
console.log('3. Enter birth details and select different Ayanamsas');
console.log('4. Look for these DEBUG logs:');
console.log('   - "DEBUG: BirthData updated:"');
console.log('   - "DEBUG: Fetching chart1 with ayanamsa:"');
console.log('   - "DEBUG: API Call getRasiChart:"');
console.log('');
console.log('5. Verify the ayanamsa value changes in the logs');
console.log('6. Check the "Active Ayanamsa:" badge in the Charts tab');
console.log('');
console.log('If you don\'t see DEBUG logs, the frontend code hasn\'t updated.');
console.log('Try restarting the frontend server.');
