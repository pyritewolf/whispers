import type { ChatConfig, User } from "./entities";

export enum InputType {
  text = "text",
  number = "number",
  url = "url",
  password = "password",
}

export enum ButtonType {
  submit = "submit",
  button = "button",
}

export type IconName = NormalIcon | BrandIcon;

export enum NormalIcon {
  trash = "trash",
  edit = "edit",
  send = "paper-plane",
  mail_bulk = "mail-bulk",
  close = "times",
  newspaper = "newspaper",
  thumbs_up = "thumbs-up",
  skull_crossbones = "skull-crossbones",
  comments = "comments",
  copy = "copy",
}

export enum BrandIcon {
  youtube = "youtube",
  twitch = "twitch",
  github = "github",
}

export enum Size {
  sm = "small",
  md = "medium",
}

export enum Gap {
  xs = "--gap-xs",
  sm = "--gap-sm",
  md = "--gap-md",
  lg = "--gap-lg",
  xl = "--gap-xl",
}

export enum Color {
  gray = "--gray",
  lighterGray = "--lighter-gray",
  secondary = "--secondary",
  primary = "--primary",
  error = "--error",
  white = "--white",
  transparent = "--transparent",
  youtube = "--youtube",
  twitch = "--twitch",
}

export enum APIStatus {
  ok = "ok",
  error = "error",
}

export type APIResponse = {
  status: APIStatus;
  body: Array<APIError> | User | ChatConfig | string;
};

export type APIError = {
  loc: Array<string>;
  msg: string;
};

export const getErrorFor = (key: string, errors: Array<APIError> | null) => {
  if (!errors) return;
  const error = errors.find((e) => e.loc.includes(key));
  if (!error) return null;
  return error.msg;
};
