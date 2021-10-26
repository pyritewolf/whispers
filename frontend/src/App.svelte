<script lang="ts">
  import { Router, Route } from "svelte-navigator";
  import { paths } from "./constants";
  import { user } from "./stores";
  import {
    Home,
    OauthCallback,
    SignIn,
    PasswordRecovery,
    Onboarding,
    Register,
    SetNewPassword,
    Chat,
  } from "./views";
</script>

<style>
</style>

<Router>
  {#if $user}
    <Route path={paths.HOME}>
      <Home />
    </Route>
    <Route path={paths.OAUTH_GOOGLE_CALLBACK}>
      <OauthCallback name="Youtube" path="google" />
    </Route>
    <Route path={paths.OAUTH_TWITCH_CALLBACK}>
      <OauthCallback name="Twitch" path="twitch" />
    </Route>
    <Route path={`${paths.CHAT}`}>
      <Chat token={$user.token} />
    </Route>
  {:else}
    <Route path={paths.REGISTER} component={Register} />
  {/if}
  <Route path={paths.PASSWORD_RECOVERY} component={PasswordRecovery} />
  <Route path={paths.NEW_PASSWORD} component={SetNewPassword} />
  <Route path={paths.SIGN_IN} component={SignIn} />
  <Route path={paths.ONBOARDING} component={Onboarding} />
  <Route path={`${paths.CHAT}/:token`} let:params>
    <Chat token={params.token} withLayout={false} withInput={false} />
  </Route>
</Router>
