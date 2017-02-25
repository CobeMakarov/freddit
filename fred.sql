--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: chat_config; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE chat_config (
    id integer NOT NULL,
    last_bulk_save timestamp without time zone DEFAULT (now())::timestamp without time zone,
    last_bulk_clean timestamp without time zone DEFAULT (now())::timestamp without time zone
);


ALTER TABLE chat_config OWNER TO obiwan;

--
-- Name: chat_config_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE chat_config_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE chat_config_id_seq OWNER TO obiwan;

--
-- Name: chat_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE chat_config_id_seq OWNED BY chat_config.id;


--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE chat_messages (
    id integer NOT NULL,
    user_id integer,
    user_name text NOT NULL,
    message_text text NOT NULL,
    date_posted timestamp without time zone DEFAULT (now())::timestamp without time zone,
    is_admin integer DEFAULT 0
);


ALTER TABLE chat_messages OWNER TO obiwan;

--
-- Name: chat_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE chat_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE chat_messages_id_seq OWNER TO obiwan;

--
-- Name: chat_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE chat_messages_id_seq OWNED BY chat_messages.id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE comments (
    id integer NOT NULL,
    post_id integer NOT NULL,
    parent integer DEFAULT 0,
    vote_count integer DEFAULT 0,
    text text NOT NULL,
    user_id integer NOT NULL,
    date_posted timestamp without time zone DEFAULT (now())::timestamp without time zone
);


ALTER TABLE comments OWNER TO obiwan;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_id_seq OWNER TO obiwan;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE comments_id_seq OWNED BY comments.id;


--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE posts_id_seq OWNER TO obiwan;

--
-- Name: posts; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE posts (
    id integer DEFAULT nextval('posts_id_seq'::regclass) NOT NULL,
    title text NOT NULL,
    subfreddit integer NOT NULL,
    type integer DEFAULT 0,
    media_url text,
    vote_count integer DEFAULT 0,
    post_text text,
    date_posted timestamp without time zone DEFAULT (now())::timestamp without time zone,
    user_id integer NOT NULL
);


ALTER TABLE posts OWNER TO obiwan;

--
-- Name: subfreddit_flairs; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE subfreddit_flairs (
    id integer NOT NULL,
    subfreddit_id integer,
    label_type text DEFAULT 'label-default'::text NOT NULL,
    text text NOT NULL
);


ALTER TABLE subfreddit_flairs OWNER TO obiwan;

--
-- Name: subfreddit_flairs_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE subfreddit_flairs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subfreddit_flairs_id_seq OWNER TO obiwan;

--
-- Name: subfreddit_flairs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE subfreddit_flairs_id_seq OWNED BY subfreddit_flairs.id;


--
-- Name: subfreddits; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE subfreddits (
    id integer NOT NULL,
    path text NOT NULL,
    title text NOT NULL,
    creator_id integer NOT NULL,
    private integer DEFAULT 0,
    description text
);


ALTER TABLE subfreddits OWNER TO obiwan;

--
-- Name: subfreddits_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE subfreddits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subfreddits_id_seq OWNER TO obiwan;

--
-- Name: subfreddits_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE subfreddits_id_seq OWNED BY subfreddits.id;


--
-- Name: subfreddits_moderators; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE subfreddits_moderators (
    id integer NOT NULL,
    subfreddit_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE subfreddits_moderators OWNER TO obiwan;

--
-- Name: subfreddits_moderators_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE subfreddits_moderators_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subfreddits_moderators_id_seq OWNER TO obiwan;

--
-- Name: subfreddits_moderators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE subfreddits_moderators_id_seq OWNED BY subfreddits_moderators.id;


--
-- Name: user_flairs; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE user_flairs (
    id integer NOT NULL,
    user_id integer,
    subfreddit_id integer,
    flair_id integer
);


ALTER TABLE user_flairs OWNER TO obiwan;

--
-- Name: user_flairs_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE user_flairs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_flairs_id_seq OWNER TO obiwan;

--
-- Name: user_flairs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE user_flairs_id_seq OWNED BY user_flairs.id;


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO obiwan;

--
-- Name: user_subfreddits_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE user_subfreddits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_subfreddits_id_seq OWNER TO obiwan;

--
-- Name: user_subfreddits; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE user_subfreddits (
    id integer DEFAULT nextval('user_subfreddits_id_seq'::regclass) NOT NULL,
    user_id integer NOT NULL,
    subfreddit_id integer NOT NULL
);


ALTER TABLE user_subfreddits OWNER TO obiwan;

--
-- Name: user_vote_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE user_vote_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_vote_id_seq OWNER TO obiwan;

--
-- Name: user_votes_comments; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE user_votes_comments (
    id integer NOT NULL,
    comment_id integer NOT NULL,
    user_id integer NOT NULL,
    vote integer DEFAULT 0
);


ALTER TABLE user_votes_comments OWNER TO obiwan;

--
-- Name: user_votes_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: obiwan
--

CREATE SEQUENCE user_votes_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_votes_comments_id_seq OWNER TO obiwan;

--
-- Name: user_votes_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: obiwan
--

ALTER SEQUENCE user_votes_comments_id_seq OWNED BY user_votes_comments.id;


--
-- Name: user_votes_posts; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE user_votes_posts (
    id integer DEFAULT nextval('user_vote_id_seq'::regclass) NOT NULL,
    post_id integer,
    user_id integer,
    vote integer DEFAULT 0
);


ALTER TABLE user_votes_posts OWNER TO obiwan;

--
-- Name: users; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE users (
    id integer DEFAULT nextval('user_id_seq'::regclass) NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    username text NOT NULL,
    night_mode integer DEFAULT 0,
    admin integer DEFAULT 0
);


ALTER TABLE users OWNER TO obiwan;

--
-- Name: chat_config id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY chat_config ALTER COLUMN id SET DEFAULT nextval('chat_config_id_seq'::regclass);


--
-- Name: chat_messages id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY chat_messages ALTER COLUMN id SET DEFAULT nextval('chat_messages_id_seq'::regclass);


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY comments ALTER COLUMN id SET DEFAULT nextval('comments_id_seq'::regclass);


--
-- Name: subfreddit_flairs id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddit_flairs ALTER COLUMN id SET DEFAULT nextval('subfreddit_flairs_id_seq'::regclass);


--
-- Name: subfreddits id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits ALTER COLUMN id SET DEFAULT nextval('subfreddits_id_seq'::regclass);


--
-- Name: subfreddits_moderators id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits_moderators ALTER COLUMN id SET DEFAULT nextval('subfreddits_moderators_id_seq'::regclass);


--
-- Name: user_flairs id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_flairs ALTER COLUMN id SET DEFAULT nextval('user_flairs_id_seq'::regclass);


--
-- Name: user_votes_comments id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_comments ALTER COLUMN id SET DEFAULT nextval('user_votes_comments_id_seq'::regclass);


--
-- Data for Name: chat_config; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY chat_config (id, last_bulk_save, last_bulk_clean) FROM stdin;
1	2017-02-22 21:39:05.330189	2017-02-22 22:13:04.064529
\.


--
-- Name: chat_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('chat_config_id_seq', 1, true);


--
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY chat_messages (id, user_id, user_name, message_text, date_posted, is_admin) FROM stdin;
1	11	fred	ooooh boi	2017-02-22 22:04:43.661741	0
2	8	saintpablo	ryan bruh can u hear me	2017-02-22 22:05:45.322231	1
3	8	saintpablo	no i cannot hear u breh	2017-02-22 22:07:32.172313	1
4	11	fred	but why	2017-02-22 22:07:32.172313	0
5	8	saintpablo	one more time man	2017-02-22 22:11:53.337406	1
6	11	fred	nah breh	2017-02-22 22:11:53.337406	0
7	8	saintpablo	hello	2017-02-22 22:16:59.539844	1
\.


--
-- Name: chat_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('chat_messages_id_seq', 7, true);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY comments (id, post_id, parent, vote_count, text, user_id, date_posted) FROM stdin;
3	9	0	0	response3	8	2017-02-20 15:40:54.418285
4	9	3	0	response to a response	8	2017-02-20 15:50:55.711157
5	9	0	0	asdf	8	2017-02-20 15:57:40.15589
6	9	4	0	response to a response to a response	8	2017-02-20 15:58:27.011592
7	9	2	0	wooo x2	8	2017-02-20 16:06:55.242816
2	9	0	-1	wooooo	8	2017-02-20 14:18:42.704594
8	9	1	-1	damn str8	8	2017-02-20 16:07:50.107915
1	9	0	2	he sure is, buddy	8	2017-02-20 00:46:31.746259
\.


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('comments_id_seq', 8, true);


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY posts (id, title, subfreddit, type, media_url, vote_count, post_text, date_posted, user_id) FROM stdin;
9	brady da goat	13	0		1	5 rings bois	2017-02-20 00:32:02.772549	8
3	This is my first post!	13	0	\N	1	This is the post content of my first post!	2017-02-13 14:34:24.074032	8
4	This is my second post!	13	0	\N	-1	This is the post content of my first post!	2017-02-13 14:35:55.967019	8
\.


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('posts_id_seq', 9, true);


--
-- Data for Name: subfreddit_flairs; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY subfreddit_flairs (id, subfreddit_id, label_type, text) FROM stdin;
\.


--
-- Name: subfreddit_flairs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('subfreddit_flairs_id_seq', 1, false);


--
-- Data for Name: subfreddits; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY subfreddits (id, path, title, creator_id, private, description) FROM stdin;
13	patriots	New England Patriots	8	0	Discussion about the greatest team in the NFL
14	nba	National Basketball Association	8	0	The subfreddit for the NBA
12	nfl	Natioanl Football League	8	0	The subfreddit for the NFL
15	fred	Fred	11	0	freddit sub
\.


--
-- Name: subfreddits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('subfreddits_id_seq', 15, true);


--
-- Data for Name: subfreddits_moderators; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY subfreddits_moderators (id, subfreddit_id, user_id) FROM stdin;
1	12	8
2	13	8
3	14	8
4	15	11
\.


--
-- Name: subfreddits_moderators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('subfreddits_moderators_id_seq', 4, true);


--
-- Data for Name: user_flairs; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY user_flairs (id, user_id, subfreddit_id, flair_id) FROM stdin;
\.


--
-- Name: user_flairs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_flairs_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_id_seq', 11, true);


--
-- Data for Name: user_subfreddits; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY user_subfreddits (id, user_id, subfreddit_id) FROM stdin;
3	8	12
4	8	13
5	8	14
6	11	15
\.


--
-- Name: user_subfreddits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_subfreddits_id_seq', 6, true);


--
-- Name: user_vote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_vote_id_seq', 35, true);


--
-- Data for Name: user_votes_comments; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY user_votes_comments (id, comment_id, user_id, vote) FROM stdin;
2	1	8	1
3	2	8	0
4	8	8	0
\.


--
-- Name: user_votes_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_votes_comments_id_seq', 4, true);


--
-- Data for Name: user_votes_posts; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY user_votes_posts (id, post_id, user_id, vote) FROM stdin;
35	9	8	1
27	3	8	1
28	4	8	0
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY users (id, email, password, username, night_mode, admin) FROM stdin;
9	troylaskiewcz@gmail.com	pbkdf2:sha1:1000$TxaoVMKw$b81c45db478f2a83dbf2270dfd6e021266489d96	Tree	1	0
10	tb12@ua.com	pbkdf2:sha1:1000$fiep433U$5407791f48264de2123a1e8761e9dc4beb4808fa	TomBrady12	1	0
11	fred@me.com	pbkdf2:sha1:1000$XDlCNAmL$195d81060bcdf5678ba734acda44915d98c7a549	fred	0	0
8	sjohns23@umw.edu	pbkdf2:sha1:1000$dLkrCuCW$bf73d94469afb62c1c58fad4d4ee1c999040fb37	saintpablo	0	1
\.


--
-- Name: chat_config chat_config_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY chat_config
    ADD CONSTRAINT chat_config_pkey PRIMARY KEY (id);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: subfreddit_flairs subfreddit_flairs_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddit_flairs
    ADD CONSTRAINT subfreddit_flairs_pkey PRIMARY KEY (id);


--
-- Name: subfreddits_moderators subfreddits_moderators_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits_moderators
    ADD CONSTRAINT subfreddits_moderators_pkey PRIMARY KEY (id);


--
-- Name: subfreddits subfreddits_name_key; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits
    ADD CONSTRAINT subfreddits_name_key UNIQUE (path);


--
-- Name: subfreddits subfreddits_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits
    ADD CONSTRAINT subfreddits_pkey PRIMARY KEY (id);


--
-- Name: user_flairs user_flairs_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_flairs
    ADD CONSTRAINT user_flairs_pkey PRIMARY KEY (id);


--
-- Name: user_subfreddits user_subfreddits_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_subfreddits
    ADD CONSTRAINT user_subfreddits_pkey PRIMARY KEY (id);


--
-- Name: user_votes_comments user_votes_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_comments
    ADD CONSTRAINT user_votes_comments_pkey PRIMARY KEY (id);


--
-- Name: user_votes_posts user_votes_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_posts
    ADD CONSTRAINT user_votes_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: chat_messages chat_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY chat_messages
    ADD CONSTRAINT chat_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts(id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: posts posts_subfreddit_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_subfreddit_fkey FOREIGN KEY (subfreddit) REFERENCES subfreddits(id);


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: subfreddit_flairs subfreddit_flairs_subfreddit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddit_flairs
    ADD CONSTRAINT subfreddit_flairs_subfreddit_id_fkey FOREIGN KEY (subfreddit_id) REFERENCES subfreddits(id);


--
-- Name: subfreddits subfreddits_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits
    ADD CONSTRAINT subfreddits_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES users(id);


--
-- Name: subfreddits_moderators subfreddits_moderators_subfreddit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits_moderators
    ADD CONSTRAINT subfreddits_moderators_subfreddit_id_fkey FOREIGN KEY (subfreddit_id) REFERENCES subfreddits(id);


--
-- Name: subfreddits_moderators subfreddits_moderators_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits_moderators
    ADD CONSTRAINT subfreddits_moderators_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: user_flairs user_flairs_flair_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_flairs
    ADD CONSTRAINT user_flairs_flair_id_fkey FOREIGN KEY (flair_id) REFERENCES subfreddit_flairs(id);


--
-- Name: user_flairs user_flairs_subfreddit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_flairs
    ADD CONSTRAINT user_flairs_subfreddit_id_fkey FOREIGN KEY (subfreddit_id) REFERENCES subfreddits(id);


--
-- Name: user_flairs user_flairs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_flairs
    ADD CONSTRAINT user_flairs_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: user_subfreddits user_subfreddits_subfreddit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_subfreddits
    ADD CONSTRAINT user_subfreddits_subfreddit_id_fkey FOREIGN KEY (subfreddit_id) REFERENCES subfreddits(id);


--
-- Name: user_subfreddits user_subfreddits_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_subfreddits
    ADD CONSTRAINT user_subfreddits_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: user_votes_comments user_votes_comments_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_comments
    ADD CONSTRAINT user_votes_comments_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES comments(id);


--
-- Name: user_votes_comments user_votes_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_comments
    ADD CONSTRAINT user_votes_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: user_votes_posts user_votes_posts_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_posts
    ADD CONSTRAINT user_votes_posts_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts(id);


--
-- Name: user_votes_posts user_votes_posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_posts
    ADD CONSTRAINT user_votes_posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- PostgreSQL database dump complete
--

