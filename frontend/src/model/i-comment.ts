import { IDiscipline } from "./i-discipline";
import { IUser } from "./i-user";

export interface IComment {
    id: number;
    content: string;
    rating: 1 | 2 | 3 | 4 | 5;
    created_at: string;
    author: IUser;
    discipline: number | IDiscipline;
    likes_count: number;
    dislikes_count: number;
}