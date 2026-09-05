import { createClient } from "matrix-js-sdk";
import type { MatrixClient } from "matrix-js-sdk";

export async function matrixLogin(
  homeserver: string,
  user: string,
  password: string
): Promise<MatrixClient> {
  const client = createClient({ baseUrl: homeserver });

  console.log(homeserver, user, password);

  const resp = await client.loginRequest({
    type: "m.login.password",
    identifier: {
      type: "m.id.user",
      user
    },
    password
  });

  return createClient({
    baseUrl: homeserver,
    accessToken: resp.access_token,
    userId: resp.user_id
  });
}
