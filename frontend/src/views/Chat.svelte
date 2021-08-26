<script lang="ts">
  import { onDestroy } from "svelte";
  import Button from "../components/Button.svelte";
  import Icon from "../components/Icon.svelte";
  import { Color, APIStatus, NormalIcon, Gap } from "../types/components";
  import { api, chat } from "../stores";
  import Input from "../components/Input.svelte";
  import ChatMessages from "../components/ChatMessages.svelte";

  export let withLayout: boolean = true;
  export let withInput: boolean = true;
  export let token: string;
  export let maxHeight: string = "100vh";

  let socket: WebSocket;
  let newMessage: string = "";

  const isStreamerOn = async () => {
    const response = await $api(`/live/is_chat_open`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === APIStatus.ok)
      socket = chat.setUpSocket(response.body, token);
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
    height: calc(var(--maxHeight) - var(--wrappers));
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

  .chat {
    height: calc(100% - var(--input));
  }
</style>

<div
  class="root"
  style="--wrappers: {(withLayout && 'calc(6.5rem + var(--gap-lg) * 2)') || '0rem'}; --input: {(withInput && '7.9rem') || '0rem'}; --maxHeight: {maxHeight};">
  {#await promise}
    <div class="center">
      <Icon name={NormalIcon.comments} size={Gap.xl} />
      <p>Loading...</p>
    </div>
  {:then response}
    {#if response.status === APIStatus.ok}
      <div class="chat">
        <ChatMessages />
      </div>
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
