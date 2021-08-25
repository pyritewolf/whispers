const fallbackCopyTextToClipboard = (text: string) => {
  const textArea = document.createElement("textarea");
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  document.execCommand("copy");
  document.body.removeChild(textArea);
};

export const copyToClipboard = async (text: string) => {
  if (!navigator.clipboard) fallbackCopyTextToClipboard(text);
  else navigator.clipboard.writeText(text);
};
