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
-- Name: comments; Type: TABLE; Schema: public; Owner: obiwan
--

CREATE TABLE comments (
    id integer NOT NULL,
    post_id integer NOT NULL,
    parent integer,
    vote_count integer DEFAULT 0,
    text text NOT NULL,
    user_id integer NOT NULL
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
    post_text text DEFAULT ''''''::text,
    date_posted timestamp without time zone DEFAULT now(),
    user_id integer NOT NULL
);


ALTER TABLE posts OWNER TO obiwan;

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
    user_id integer NOT NULL
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
    user_id integer
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
    night_mode integer DEFAULT 0
);


ALTER TABLE users OWNER TO obiwan;

--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY comments ALTER COLUMN id SET DEFAULT nextval('comments_id_seq'::regclass);


--
-- Name: subfreddits id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits ALTER COLUMN id SET DEFAULT nextval('subfreddits_id_seq'::regclass);


--
-- Name: subfreddits_moderators id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY subfreddits_moderators ALTER COLUMN id SET DEFAULT nextval('subfreddits_moderators_id_seq'::regclass);


--
-- Name: user_votes_comments id; Type: DEFAULT; Schema: public; Owner: obiwan
--

ALTER TABLE ONLY user_votes_comments ALTER COLUMN id SET DEFAULT nextval('user_votes_comments_id_seq'::regclass);


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY comments (id, post_id, parent, vote_count, text, user_id) FROM stdin;
\.


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('comments_id_seq', 0, false);


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY posts (id, title, subfreddit, type, media_url, vote_count, post_text, date_posted, user_id) FROM stdin;
\.


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('posts_id_seq', 0, false);

--
-- Name: subfreddits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('subfreddits_id_seq', 0, true);

--
-- Name: subfreddits_moderators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('subfreddits_moderators_id_seq', 0, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_id_seq', 0, true);

--
-- Name: user_subfreddits_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_subfreddits_id_seq', 0, true);


--
-- Name: user_vote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_vote_id_seq', 0, false);


--
-- Data for Name: user_votes_comments; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY user_votes_comments (id, comment_id, user_id) FROM stdin;
\.


--
-- Name: user_votes_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: obiwan
--

SELECT pg_catalog.setval('user_votes_comments_id_seq', 1, false);


--
-- Data for Name: user_votes_posts; Type: TABLE DATA; Schema: public; Owner: obiwan
--

COPY user_votes_posts (id, post_id, user_id) FROM stdin;
\.

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

