import { writable } from "svelte/store";
import type { User } from "../types/entities";

const user = () => {
  const { subscribe, set } = writable(
    JSON.parse(localStorage.getItem("user")) || null
  );

  const setWithLocalStorage = (value: User | null) => {
    if (value) localStorage.setItem("user", JSON.stringify(value));
    else localStorage.removeItem("user");
    set(value);
  };
  return {
    subscribe,
    set: setWithLocalStorage,
    update: (fn: Function) =>
      setWithLocalStorage(fn(JSON.parse(localStorage.getItem("user")))),
  };
};

export default user();
