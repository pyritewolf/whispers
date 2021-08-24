<script lang="ts">
  import { onMount } from "svelte";
  import Button from "../components/Button.svelte";
  import Icon from "../components/Icon.svelte";
  import { ButtonType, BrandIcon, Color } from "../types/components";
  import { user } from "../stores";
  import Chat from "./Chat.svelte";

  let youtubeColor: Color = Color.youtube;
  let youtubeText: string = "Link your Youtube account";
  let twitchColor: Color = Color.twitch;
  let twitchText: string = "Link your Twitch account";

  onMount(() => {
    if (!$user.hasYoutubeAuth) return;
    youtubeColor = Color.gray;
    youtubeText = "Your Youtube account is linked (click to re-link)";
  });
</script>

<style>
  .root {
    display: flex;
    gap: var(--gap-lg);
  }

  section {
    width: 100%;
  }

  .chat {
    background-color: var(--dark-gray);
    border-radius: var(--radius);
    margin-top: var(--gap-md);
  }

  aside {
    width: 45rem;
  }
</style>

<div class="root">
  <section>
    <h1>Your chat</h1>
    <div class="chat">
      {#if $user.hasYoutubeAuth}
        <Chat
          maxHeight="30rem"
          withLayout={false}
          withInput={false}
          streamer={$user.username} />
      {:else}
        <p>Your account isn't linked to Youtube!</p>
      {/if}
    </div>
  </section>
  <aside>
    <Button
      type={ButtonType.button}
      color={youtubeColor}
      click={() => window.location.replace('/api/auth/google')}>
      <Icon name={BrandIcon.youtube} />
      {youtubeText}
    </Button>
    <Button
      type={ButtonType.button}
      color={twitchColor}
      click={() => window.location.replace('/api/auth/google')}>
      <Icon name={BrandIcon.twitch} />
      {twitchText}
    </Button>
  </aside>
</div>
