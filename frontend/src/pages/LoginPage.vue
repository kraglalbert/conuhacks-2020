<template>
  <q-layout>
    <q-page-container>
      <!-- PUT APP NAME HERE -->
      <q-banner class="login_banner">
        <div style="font-size: 25px; font-weight: bold;">Wellness Hub</div>
      </q-banner>

      <q-page class="flex column flex-center login_page">
        <div
          class="q-gutter-y-md"
          style="min-width: 300px"
        >
          <!-- ee8572 -->
          <q-card>
            <q-tabs
              v-model="tab"
              dense
              class="text-grey"
              active-color="primary"
              indicator-color="primary"
              align="justify"
              narrow-indicator
            >
              <q-tab
                name="login"
                label="Log In"
              />
              <q-tab
                name="signup"
                label="Sign Up"
              />
            </q-tabs>

            <q-separator />

            <q-tab-panels
              v-model="tab"
              animated
            >
              <q-tab-panel name="login">
                <q-form
                  @submit="onLogIn"
                  class="q-gutter-md"
                >
                  <q-input
                    filled
                    v-model="email"
                    label="Email"
                    hint="Enter your email"
                    lazy-rules
                    :rules="[
                      val =>
                        (val && val.length > 0) || 'Please enter your email'
                    ]"
                  />

                  <q-input
                    filled
                    v-model="password"
                    label="Password"
                    type="password"
                    hint="Enter your password"
                    lazy-rules
                    :rules="[
                      val =>
                        (val !== null && val !== '') ||
                        'Please enter your password'
                    ]"
                  />

                  <div>
                    <q-btn
                      label="Log In"
                      type="submit"
                      style="background:#678a74; color:white"
                    />
                  </div>
                </q-form>
              </q-tab-panel>

              <q-tab-panel name="signup">
                <q-form
                  @submit="onSignUp"
                  class="q-gutter-md"
                >
                  <q-input
                    filled
                    v-model="name"
                    label="Name"
                    hint="Enter your name"
                    lazy-rules
                    :rules="[
                      val => (val && val.length > 0) || 'Please enter your name'
                    ]"
                  />
                  <q-input
                    filled
                    v-model="email"
                    label="Email"
                    hint="Enter your email"
                    lazy-rules
                    :rules="[
                      val =>
                        (val && val.length > 0) || 'Please enter your email'
                    ]"
                  />
                  <q-input
                    filled
                    v-model="location"
                    label="Location"
                    hint="Enter your location"
                    lazy-rules
                    :rules="[
                      val =>
                        (val && val.length > 0) || 'Please enter your location'
                    ]"
                  />
                  <q-input
                    filled
                    v-model="company"
                    label="Company"
                    hint="Enter your company"
                    lazy-rules
                    :rules="[
                      val =>
                        (val && val.length > 0) || 'Please enter your company'
                    ]"
                  />
                  <q-input
                    filled
                    v-model="password"
                    label="Password"
                    type="password"
                    hint="Enter your password"
                    lazy-rules
                    :rules="[
                      val =>
                        (val !== null && val !== '') ||
                        'Please enter your password'
                    ]"
                  />

                  <q-input
                    filled
                    v-model="confirm_password"
                    label="Confirm Password"
                    type="password"
                    hint="Confirm your password"
                    lazy-rules
                    :rules="[
                      val =>
                        (val !== null && val !== '') ||
                        'Please confirm your password',
                      val => val === password || 'Passwords do not match'
                    ]"
                  />

                  <div>
                    <q-btn
                      label="Sign Up"
                      type="submit"
                      style="background:#678a74; color:white"
                    />
                  </div>
                </q-form>
              </q-tab-panel>
            </q-tab-panels>
          </q-card>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "LoginPage",
  data () {
    return {
      name: null,
      email: null,
      password: null,
      confirm_password: null,
      company: null,
      location: null,
      tab: "login"
    };
  },
  methods: {
    onLogIn () {
      let email = this.email;
      let password = this.password;
      this.$store
        .dispatch("login", { email, password })
        .then(() => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Logged in successfully"
          });
          this.$router.push({ path: "/home" });
        })
        .catch(_err => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Wrong email or password"
          });
        });
    },
    onSignUp () {
      let name = this.name;
      let email = this.email;
      let password = this.password;
      let company = this.company;
      let location = this.location;
      this.$store
        .dispatch("register", { name, email, password, company, location })
        .then(() => {
          this.$q.notify({
            color: "green-4",
            position: "top",
            textColor: "white",
            icon: "cloud_done",
            message: "Registered successfully"
          });
          this.$router.push({ path: "/home" });
        })
        .catch(_err => {
          this.$q.notify({
            color: "red-4",
            position: "top",
            textColor: "white",
            icon: "error",
            message: "Sign Up Error"
          });
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.login_banner {
  background-color: $secondary;
  color: white;
}
.login_page {
  background-color: $background;
}
</style>
