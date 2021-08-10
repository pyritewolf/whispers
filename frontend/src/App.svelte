<script lang="ts">
  import { Router, Link, Route } from "svelte-navigator";
  import { paths } from "./constants";

  import Home from "./views/Home.svelte";
  import SignIn from "./views/SignIn.svelte";
  import Onboarding from "./views/Onboarding.svelte";
  import Register from "./views/Register.svelte";

  export let name: string;
</script>

<style>
</style>

<main>
  <h1>Hello {name}!</h1>
  <Router>
    <nav>
      <Link to={paths.HOME}>Home</Link>
      <Link to={paths.SIGN_IN}>Sign in</Link>
      <Link to={paths.REGISTER}>Register</Link>
    </nav>
    <div>
      <Route path={paths.HOME}>
        <Home />
      </Route>
      <Route path={paths.SIGN_IN} component={SignIn} />
      <Route path={paths.REGISTER} component={Register} />
      <Route path={paths.ONBOARDING} component={Onboarding} />
    </div>
  </Router>
</main>
