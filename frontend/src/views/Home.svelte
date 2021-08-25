<script lang="ts">
  import { onMount } from "svelte";
  import Button from "../components/Button.svelte";
  import Icon from "../components/Icon.svelte";
  import { ButtonType, BrandIcon, Color, Size } from "../types/components";
  import { user } from "../stores";
  import { copyToClipboard } from "../utils";
  import Chat from "./Chat.svelte";
  import Input from "../components/Input.svelte";

  let youtubeColor: Color = Color.youtube;
  let youtubeText: string = "Link your Youtube account";
  let twitchColor: Color = Color.twitch;
  let twitchText: string = "Link your Twitch account";

  onMount(() => {
    if (!$user.hasYoutubeAuth) return;
    youtubeColor = Color.gray;
    youtubeText = "Click to refresh your Youtube auth";
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
    padding: var(--gap-md);
  }

  .chat .col {
    display: flex;
    gap: var(--gap-md);
    align-items: center;
  }

  .chat .col > :global(*:first-child) {
    flex-grow: 1;
  }

  .chat .col > :global(*:last-child) {
    width: 15rem;
  }

  aside {
    width: 45rem;
    display: flex;
    gap: var(--gap-md);
    flex-direction: column;
  }
</style>

<div class="root">
  <section>
    <h1>Your chat</h1>
    <div class="chat">
      {#if $user.hasYoutubeAuth}
        <div class="col">
          <Input
            label="OBS Embed Link"
            help="Click to copy your embed link"
            value={$user.chatEmbedSecret || 'banana'}
            readonly={true}
            click={() => copyToClipboard($user.chatEmbedSecret)} />
          <Button>Get new link</Button>
        </div>
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
