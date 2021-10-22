import { writable } from "svelte/store";
import type { ChatConfig } from "../types/entities";

const messageStore = writable([]);

const sendMessage = (message, socket) => {
  if (socket.readyState <= 1) socket.send(message);
};

const clearMessages = (messages) => {
  setTimeout(() => {
    messageStore.update((msgs) =>
      msgs.map((message) => {
        if (messages.includes(message)) message.fade = new Date();
        return message;
      })
    );
  }, 10000);
};

const setUpSocket = (
  configs: ChatConfig,
  token: string,
  autoClearMessages: boolean = true
) => {
  let socket = new WebSocket(
    `ws://${configs.serverUrl}/api/live/chat/${token}?youtube_chat_id=${configs.youtubeChatId}`
  );

  // Connection opened
  socket.addEventListener("open", () => {
    const msg = { text: "The chat is connected!" };
    messageStore.update((messages) => [...messages, msg]);
    if (!autoClearMessages) return;
    clearMessages([msg]);
  });

  // Listen for messages
  socket.addEventListener("message", (event) => {
    let newMessages = JSON.parse(event.data);
    messageStore.update((messages) => [
      ...messages.filter(
        (message) =>
          !("fade" in message) ||
          Math.floor((new Date().getTime() - message.fade.getTime()) / 1000) <=
            1
      ),
      ...newMessages,
    ]);
    if (!autoClearMessages) return;
    clearMessages(newMessages);
  });

  // Connection opened
  socket.onclose = () => {
    messageStore.update((messages) => [
      ...messages,
      { text: "The chat has disconnected. Try reloading!" },
    ]);
  };
  return socket;
};

export default {
  subscribe: messageStore.subscribe,
  update: messageStore.update,
  sendMessage,
  setUpSocket,
};
