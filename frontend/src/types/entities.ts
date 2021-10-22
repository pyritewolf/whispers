export type User = {
  id: number;
  email: string;
  username: string;
  token: string;
  hasYoutubeAuth: boolean;
  chatEmbedSecret: string | null;
};

export type ChatConfig = {
  serverUrl: string;
  youtubeChatId: string;
};
