<script lang="ts">
  import { onDestroy } from "svelte";
  import Button from "../components/Button.svelte";
  import Icon from "../components/Icon.svelte";
  import { Color, APIStatus, NormalIcon, Gap } from "../types/components";
  import { api, chat } from "../stores";
  import Input from "../components/Input.svelte";
  import type { ChatConfig } from "../types/entities";

  export let withLayout: boolean = true;
  export let withInput: boolean = true;
  export let streamer: string;

  let socket: WebSocket;
  let newMessage: string = "";

  const setUpSocket = (configs: ChatConfig) => {
    socket = new WebSocket(
      `ws://${configs.serverUrl}/api/live/chat/${streamer}?username=obsidianwolf&youtube_chat_id=${configs.youtubeChatId}`
    );

    // Connection opened
    socket.addEventListener("open", function (event) {
      chat.update((messages) => [
        ...messages,
        { text: "The chat is connected!" },
      ]);
    });

    // Listen for messages
    socket.addEventListener("message", function (event) {
      console.log(event.data);
      chat.update((messages) => [...messages, ...JSON.parse(event.data)]);
    });

    // Connection opened
    socket.onclose = (event) => {
      console.log(event);
      chat.update((messages) => [
        ...messages,
        { text: "The chat has disconnected. Try reloading!" },
      ]);
    };
  };

  const isStreamerOn = async () => {
    const response = await $api(`/live/is_chat_open/${streamer}`);
    if (response.status === APIStatus.ok) setUpSocket(response.body);
    return response;
  };
  const promise = isStreamerOn();

  const handleSubmit = () => {
    if (newMessage.length == 0) return;
    chat.sendMessage(newMessage, socket);
    newMessage = "";
  };

  onDestroy(() => {
    socket.close();
  });
</script>

<style>
  .root {
    height: calc(100vh - var(--wrappers));
  }

  .center {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    font-size: var(--font-lg);
    height: 100%;
  }

  form {
    display: flex;
    gap: var(--gap-md);
    align-items: center;
  }

  .input {
    width: 100%;
  }

  .button {
    width: 150px;
    display: flex;
    align-items: center;
  }

  .system {
    font-style: italic;
  }

  section {
    height: calc(100% - var(--input));
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }
</style>

<div
  class="root"
  style="--wrappers: {(withLayout && 'calc(6.5rem + var(--gap-lg) * 2)') || '0rem'}; --input: {(withInput && '7.9rem') || '0rem'};">
  {#await promise}
    <div class="center">
      <Icon name={NormalIcon.comments} size={Gap.xl} />
      <p>Loading...</p>
    </div>
  {:then response}
    {#if response.status === APIStatus.ok}
      <section>
        {#each $chat as message}
          <p class:system={!('username' in message)}>
            {#if 'username' in message}<strong>{message.username}</strong>:{/if}
            {message.text}
          </p>
        {/each}
      </section>
      <form autocomplete="off" on:submit|preventDefault={handleSubmit}>
        <div class="input">
          <Input
            name="send-message"
            placeholder="nice move!"
            bind:value={newMessage} />
        </div>
        <div class="button">
          <Button color={newMessage ? Color.primary : Color.gray}>Send</Button>
        </div>
      </form>
    {:else}
      <div class="center">
        <Icon name={NormalIcon.skull_crossbones} size={Gap.xl} />
        <p>{response.body}</p>
      </div>
    {/if}
  {/await}
</div>
