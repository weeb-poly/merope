import { matrixLogin } from "./util/matrix.ts";
import * as inviteCog from "./cogs/invite.ts";
import { getMatrixCreds } from "./util/secrets.ts";

// !admin users create-user ${MATRIX_USER}
// !admin users reset_password ${MATRIX_USER}

const { user, password, homeserver } = await getMatrixCreds();

const client = await matrixLogin(homeserver, user, password);

inviteCog.register(client);

await client.startClient();
