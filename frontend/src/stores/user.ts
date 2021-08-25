import { writable } from "svelte/store";
import type { User } from "../types/entities";

const user = () => {
  const { subscribe, set, update } = writable(
    JSON.parse(localStorage.getItem("user")) || null
  );

  return {
    subscribe,
    set: (value: User | null) => {
      if (value) localStorage.setItem("user", JSON.stringify(value));
      else localStorage.removeItem("user");
      set(value);
    },
    update,
  };
};

export default user();
