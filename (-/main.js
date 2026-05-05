const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow(type) {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    title: type === 'binary' ? 'Terminal' : 'Hacking Status'
  });

  win.loadFile('index.html', { query: { type: type } });
  return win;
}

app.whenReady().then(() => {
  // Create multiple binary terminals
  for (let i = 0; i < 10; i++) {
    setTimeout(() => createWindow('binary'), i * 100);
  }

  // Create fake hacking tabs
  const messages = ['Access Granted', 'Hacking in Progress', 'System Compromised', 'Data Retrieved', 'Firewall Breached'];
  messages.forEach((msg, index) => {
    setTimeout(() => {
      const win = createWindow('message');
      win.webContents.once('did-finish-load', () => {
        win.webContents.send('set-message', msg);
      });
    }, (10 + index) * 100);
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow('binary');
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});