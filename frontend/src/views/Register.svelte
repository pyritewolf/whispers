<script lang="ts">
	import { Link } from "svelte-navigator";
  import AuthLayout from "../layouts/AuthLayout.svelte"
  import Input from "../components/Input.svelte"
  import {paths} from "../constants"

  const formData = {
    email: "",
    password: "",
    confirmPassword: "",
    username: "",
  }
</script>

<AuthLayout>
  <h1>Sign up</h1>
  <p>Already got an account? <Link to={paths.LOGIN}>Log in</Link>!</p>
  <Input label="E-mail" placeholder="coolstreamer@gmail.com" value={formData.email} name="email"/>
  <Input label="Username" placeholder="coolstreamer69" value={formData.username} name="username"/>
  <Input label="Password" placeholder="safetaters69" value={formData.password} name="password"/>
  <Input label="Repeat password" placeholder="safetaters69" value={formData.confirmPassword} name="confirm-password"/>
</AuthLayout>

<style>
  h1 {
    text-align: center;
    padding-bottom: var(--gap-md);
  }

  p {
    text-align: center;
  }
</style>
