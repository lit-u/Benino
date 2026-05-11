// Popup tik atidaro atskirą STT langą
chrome.windows.create({
  url: chrome.runtime.getURL('stt.html'),
  type: 'popup',
  width: 340,
  height: 220,
  focused: true
});
window.close();
