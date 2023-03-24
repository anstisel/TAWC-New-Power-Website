import { reactive } from "vue";

export const login_state = reactive({
  logged_in: false,
  username: null,
  user_id: null,
  token: null,
  admin: false,
  avatar: null,
});
