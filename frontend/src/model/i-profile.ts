import { IComment } from "./i-comment";

export interface IProfile {
  id: number;
  username: string;
  avatar: string | null;
  comment_count: number;
  like_count: number;
  dislike_count: number;
  comments: IComment[];
}
