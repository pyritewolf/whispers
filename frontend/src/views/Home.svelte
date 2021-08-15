<script lang="ts">
  import Button from "../components/Button.svelte";
  import Icon from "../components/Icon.svelte";
  import { ButtonType, BrandIcon, Color } from "../types/components";
</script>

<Button type={ButtonType.button} color={Color.youtube}>
  <Icon name={BrandIcon.youtube} />
  Link your Youtube account
</Button>
