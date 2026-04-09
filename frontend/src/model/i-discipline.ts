import { IComment } from "./i-comment";
import { IUser } from "./i-user";

export interface IDiscipline {
    id: number;
    name: string;
    created_at: string;
    approved_by: number | IUser;
    comment_count: number;
}
