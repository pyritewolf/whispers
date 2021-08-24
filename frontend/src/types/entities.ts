export type User = {
  id: number;
  email: string;
  username: string;
  token: string;
  hasYoutubeAuth: boolean;
};

export type ChatConfig = {
  serverUrl: string;
  youtubeChatId: string;
};
