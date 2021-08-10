import { derived } from "svelte/store";
import { paths } from "../constants";
import { APIStatus, APIResponse } from "../types/components";
import user from "./user";

export default derived(user, ($user) => {
  const method = async (
    path: string,
    options: any = { headers: {} }
  ): Promise<APIResponse | null> => {
    let user = JSON.parse(localStorage.getItem("user"));
    const opts = { ...options };
    if (user)
      opts.headers = {
        Authorization: `Bearer ${user.token}`,
        ...options.headers,
      };
    if (opts.body)
      opts.headers = {
        "Content-Type": "application/json",
        ...opts.headers,
      };
    const response = await fetch(path, opts);
    const result = {
      status: APIStatus.ok,
      body: (await response.json()) || {},
    };
    if (response.status === 401) {
      user.update(() => {
        localStorage.removeItem("user");
        return null;
      });
      window.location.replace(paths.SIGN_IN);
    }
    if (response.status < 200 || response.status >= 300)
      result.status = APIStatus.error;
    if ("details" in result.body) result.body = result.body.details;
    return result;
  };
  return method;
});
