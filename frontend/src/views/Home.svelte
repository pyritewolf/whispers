<script lang="ts">
  import { onMount } from "svelte";
  import { api } from "../stores";
  import Button from "../components/Button.svelte";
  import Icon from "../components/Icon.svelte";
  import { ButtonType, BrandIcon, Color } from "../types/components";
  import { user } from "../stores";

  let youtubeColor: Color = Color.youtube;
  let youtubeText: string = "Link your Youtube account";

  onMount(() => {
    if (!$user.hasYoutubeAuth) return;
    youtubeColor = Color.gray;
    youtubeText = "Your Youtube account is linked (click to re-link)";
  });
</script>

<Button
  type={ButtonType.button}
  color={youtubeColor}
  click={() => window.location.replace('/api/auth/google')}>
  <Icon name={BrandIcon.youtube} />
  {youtubeText}
</Button>
