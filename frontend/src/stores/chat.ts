import { writable } from "svelte/store";
import type { ChatConfig } from "../types/entities";

const messageStore = writable([]);

const sendMessage = (message, socket) => {
  if (socket.readyState <= 1) {
    socket.send(message);
  }
};

const setUpSocket = (configs: ChatConfig, streamer: string) => {
  let socket = new WebSocket(
    `ws://${configs.serverUrl}/api/live/chat/${streamer}?youtube_chat_id=${configs.youtubeChatId}`
  );

  // Connection opened
  socket.addEventListener("open", function (event) {
    messageStore.update((messages) => [
      ...messages,
      { text: "The chat is connected!" },
    ]);
  });

  // Listen for messages
  socket.addEventListener("message", function (event) {
    console.log(event.data);
    messageStore.update((messages) => [...messages, ...JSON.parse(event.data)]);
  });

  // Connection opened
  socket.onclose = (event) => {
    console.log(event);
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
