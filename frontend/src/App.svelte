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
  import PrivateRoute from "./components/PrivateRoute.svelte";
</script>

<style>
</style>

<Router>
  <PrivateRoute path={paths.HOME} component={Home} />
  <PrivateRoute path={paths.OAUTH_GOOGLE_CALLBACK}>
    <OauthCallback name="Youtube" />
  </PrivateRoute>
  <PrivateRoute path={`${paths.CHAT}`}>
    <Chat token={$user.token} />
  </PrivateRoute>
  <Route path={paths.REGISTER} component={Register} />
  <Route path={paths.PASSWORD_RECOVERY} component={PasswordRecovery} />
  <Route path={paths.NEW_PASSWORD} component={SetNewPassword} />
  <Route path={paths.SIGN_IN} component={SignIn} />
  <Route path={paths.ONBOARDING} component={Onboarding} />
  <Route path={`${paths.CHAT}/:token`} let:params>
    <Chat token={params.token} withLayout={false} withInput={false} />
  </Route>
</Router>
