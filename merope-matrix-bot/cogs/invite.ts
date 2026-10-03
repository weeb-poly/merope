import type { MatrixClient, Room, RoomMember } from "matrix-js-sdk";
import { ClientEvent, RoomStateEvent } from "matrix-js-sdk";

const tempRoomId = process.env["TEMP_ROOM"] ?? "";
const inviteRoomId = process.env["INVITE_ROOM"] ?? "";

async function tempRoomHandler(
  client: MatrixClient,
  member: RoomMember,
  inviteRoom: Room,
  tempRoom: Room,
) {
  // Only do things on member join
  if (member.membership !== "join") return;

  // User is already in the target room
  if (inviteRoom.getMember(member.userId) !== null) {
    await client.kick(tempRoom.roomId, member.userId);
    return;
  }

  // Sanity check. This shouldn't be necessary if federation is disabled
  const userHomeServer = member.userId.split(":", 2)[1];
  const inviteHomeServer = inviteRoom.roomId.split(":", 2)[1];
  if (userHomeServer !== inviteHomeServer) return;

  await client.invite(inviteRoom.roomId, member.userId);
}

async function inviteRoomHandler(
  client: MatrixClient,
  member: RoomMember,
  _inviteRoom: Room,
  tempRoom: Room,
) {
  if (member.membership !== "join") return;
  // Kick user from temp room if they're present
  if (tempRoom.getMember(member.userId) !== null) return;
  await client.kick(tempRoom.roomId, member.userId);
}

export function register(client: MatrixClient) {
  client.once(ClientEvent.Sync, async function () {
    const inviteRoom = await client.joinRoom(inviteRoomId);
    const tempRoom = await client.joinRoom(tempRoomId);

    // NOTE: RoomStateEvent.NewMember events don't seem to fire
    /*
    tempRoom.on(RoomStateEvent.NewMember, async (_event, _state, member) => {
      await tempRoomHandler(client, member, inviteRoom, tempRoom);
    });
    inviteRoom.on(RoomStateEvent.NewMember, async (_event, _state, member) => {
      await inviteRoomHandler(client, member, inviteRoom, tempRoom);
    });
    */

    // NOTE: error seems to happen on this
    tempRoom.on(RoomStateEvent.Members, async (_event, _state, member) => {
      await tempRoomHandler(client, member, inviteRoom, tempRoom).catch(console.error);;
    });
    inviteRoom.on(RoomStateEvent.Members, async (_event, _state, member) => {
      await inviteRoomHandler(client, member, inviteRoom, tempRoom).catch(console.error);;
    });
  });
}
