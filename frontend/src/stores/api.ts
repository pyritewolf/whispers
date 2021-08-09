import { derived } from "svelte/store";
import { paths } from "../constants";
import { APIStatus, APIResponse } from "../types/components";
import user from "./user";

export default derived(user, ($user) => {
  const method = async (
    path: string,
    options: any = { headers: {} }
  ): Promise<APIResponse | null> => {
    let token = localStorage.getItem("token");
    if (!token) {
      token = new URLSearchParams(window.location.search).get("token");
      if (token) localStorage.setItem("token", token);
    }
    const opts = { ...options };
    if (token)
      opts.headers = {
        Authorization: `Bearer ${token}`,
        ...options.headers,
      };
    if (opts.body)
      opts.headers = {
        "Content-Type": "application/json",
        ...opts.headers,
      };
    const response = await fetch(path, opts);
    const body = await response.json();
    if (response.status === 401) {
      user.update(() => {
        localStorage.removeItem("token");
        return null;
      });
      window.location.replace(paths.LOGIN);
    }
    let status = APIStatus.ok;
    if (response.status < 200 || response.status >= 300)
      status = APIStatus.error;
    return { status, body: body.detail };
  };
  return method;
});
