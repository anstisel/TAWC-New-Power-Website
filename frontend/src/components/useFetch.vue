<script>
import { ref } from "vue";
import axios from "axios";
import { login_state } from "@/login_state.js";

export const useFetch = (
  url,
  config = {},
  authenticate = false,
  silent = true
) => {
  const data = ref(null);
  const response = ref(null);
  const error = ref(null);
  const loading = ref(null);
  const items = ref(null);

  const fetch = async () => {
    loading.value = true;

    if (!config.method) {
      config.method = "GET";
    }
    if (!config.headers) {
      config.headers = {};
    }
    if (!config.headers["Content-Type"]) {
      config.headers["Content-Type"] = "application/json";
    }

    if (authenticate) {
      const token = login_state.token;
      config.headers["Authorization"] = token;
    }

    if (!silent) {
      console.log(config);
    }
    try {
      const result = await axios.request({
        url,
        ...config,
      });
      response.value = result;
      data.value = result.data;
      items.value = data.value.items;
    } catch (ex) {
      error.value = ex;
    } finally {
      loading.value = false;
      if (!silent) {
        console.log("API request done");
        console.log(data.value);
      }
    }
  };

  !config.skip && fetch();

  return { response, error, data, loading, items, fetch };
};

export default {
  data() {
    return {
      isAuthenticated: this.$auth0.isAuthenticated,
      isLoading: this.$auth0.isLoading,
      login_state,
      fetch_1: null,
    };
  },
  methods: {
    async getAccessToken() {
      let token;
      token = await this.$auth0.getAccessTokenSilently();
      console.log(token);
      //console.log(token);
      return token;
    },
  },
};
</script>
