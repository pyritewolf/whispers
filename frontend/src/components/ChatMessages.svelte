<script lang="ts">
  import { beforeUpdate, afterUpdate } from "svelte";
  import { chat } from "../stores";

  let chatRoot;
  let autoscroll;

  beforeUpdate(() => {
    autoscroll =
      chatRoot &&
      chatRoot.offsetHeight + chatRoot.scrollTop > chatRoot.scrollHeight - 20;
  });

  afterUpdate(() => {
    if (autoscroll) chatRoot.scrollTo(0, chatRoot.scrollHeight);
  });
</script>

<style>
  .system {
    font-style: italic;
  }

  section {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    overflow-y: auto;
    overflow-x: hidden;
  }
</style>

<section bind:this={chatRoot}>
  {#each $chat as message}
    <p class:system={!('username' in message)}>
      {#if 'username' in message}<strong>{message.username}</strong>:{/if}
      {message.text}
    </p>
  {/each}
</section>
