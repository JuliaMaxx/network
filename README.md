# Network
## Video Demo: https://www.youtube.com/watch?v=U0A9ARZ6bSU
![Screenshot (19)](https://github.com/JuliaMaxy/project4/assets/121096183/b307bf23-c22c-4c34-973a-17f5f7a4a99f)
## Description:
Design a Twitter-like social network website for making posts and following users.
## Specification:
- **`New Post`**: Users who are signed in are able to write a new text-based post by filling in text into a text area
   and then clicking a button to submit the post.
- **`All Posts`**:
  - Takes the user to a page where they can see all posts from all users, with the most recent posts first.
  - Each post includes the username of the poster,
    the post content itself, the date and time at which the post was made, and the number of “likes” the post has
- **`Profile Page`**:
  - Clicking on a username loads that user’s profile page.
  - The page displays the number of followers the user has, as well as the number of people that the user follows.
  - The page displays all of the posts for that user, in reverse chronological order.
  - For any other user who is signed in, this page also displays a `Follow` or `Unfollow` button
     that will let the current user toggle whether or not they are following this user’s posts.
     This only applies to any “other” user: a user is not able to follow themselves.
- **`Following`**: Takes the signed in user to a page where they see all posts made by users that the current user follows.
- **`Pagination`**: On any page that displays posts, posts can only be displayed 10 on a page.
  - If there are more than ten posts, a  `Next` button appears to take the user to the next page of posts.
  - If not on the first page, a `Previous` button appears to take the user to the previous page of posts as well.
- **`Edit Post`**:
  - Users can click an `Edit` button on any of their own posts to edit that post.
  - When a user clicks `Edit` for one of their own posts, the content of their post is replaced with a textarea
    where the user can edit the content of their post.
- **`Like` and `Unlike`**: Users are able to click a button on any post to toggle whether or not they `like` that post.
