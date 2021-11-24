export type User = {
  id: number;
  email: string;
  username: string;
  token: string;
  hasAuth: boolean;
  hasYoutubeAuth: boolean;
  hasTwitchAuth: boolean;
  chatEmbedSecret: string | null;
};

export type ChatConfig = {
  serverUrl: string;
  youtubeChatId: string;
};
