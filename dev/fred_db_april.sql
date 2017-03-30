--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.user_votes_posts DROP CONSTRAINT user_votes_posts_user_id_fkey;
ALTER TABLE ONLY public.user_votes_posts DROP CONSTRAINT user_votes_posts_post_id_fkey;
ALTER TABLE ONLY public.user_votes_comments DROP CONSTRAINT user_votes_comments_user_id_fkey;
ALTER TABLE ONLY public.user_votes_comments DROP CONSTRAINT user_votes_comments_comment_id_fkey;
ALTER TABLE ONLY public.user_subfreddits DROP CONSTRAINT user_subfreddits_user_id_fkey;
ALTER TABLE ONLY public.user_subfreddits DROP CONSTRAINT user_subfreddits_subfreddit_id_fkey;
ALTER TABLE ONLY public.user_flairs DROP CONSTRAINT user_flairs_user_id_fkey;
ALTER TABLE ONLY public.user_flairs DROP CONSTRAINT user_flairs_subfreddit_id_fkey;
ALTER TABLE ONLY public.user_flairs DROP CONSTRAINT user_flairs_flair_id_fkey;
ALTER TABLE ONLY public.subfreddits_moderators DROP CONSTRAINT subfreddits_moderators_user_id_fkey;
ALTER TABLE ONLY public.subfreddits_moderators DROP CONSTRAINT subfreddits_moderators_subfreddit_id_fkey;
ALTER TABLE ONLY public.subfreddits DROP CONSTRAINT subfreddits_creator_id_fkey;
ALTER TABLE ONLY public.subfreddit_flairs DROP CONSTRAINT subfreddit_flairs_subfreddit_id_fkey;
ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_user_id_fkey;
ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_subfreddit_fkey;
ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_user_id_fkey;
ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_post_id_fkey;
ALTER TABLE ONLY public.chat_messages DROP CONSTRAINT chat_messages_user_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.user_votes_posts DROP CONSTRAINT user_votes_pkey;
ALTER TABLE ONLY public.user_votes_comments DROP CONSTRAINT user_votes_comments_pkey;
ALTER TABLE ONLY public.user_subfreddits DROP CONSTRAINT user_subfreddits_pkey;
ALTER TABLE ONLY public.user_flairs DROP CONSTRAINT user_flairs_pkey;
ALTER TABLE ONLY public.subfreddits DROP CONSTRAINT subfreddits_pkey;
ALTER TABLE ONLY public.subfreddits DROP CONSTRAINT subfreddits_name_key;
ALTER TABLE ONLY public.subfreddits_moderators DROP CONSTRAINT subfreddits_moderators_pkey;
ALTER TABLE ONLY public.subfreddit_flairs DROP CONSTRAINT subfreddit_flairs_pkey;
ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_pkey;
ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_pkey;
ALTER TABLE ONLY public.chat_messages DROP CONSTRAINT chat_messages_pkey;
ALTER TABLE ONLY public.chat_config DROP CONSTRAINT chat_config_pkey;
ALTER TABLE public.user_votes_comments ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.user_flairs ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.subfreddits_moderators ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.subfreddits ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.subfreddit_flairs ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.comments ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.chat_messages ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.chat_config ALTER COLUMN id DROP DEFAULT;
DROP TABLE public.users;
DROP TABLE public.user_votes_posts;
DROP SEQUENCE public.user_votes_comments_id_seq;
DROP TABLE public.user_votes_comments;
DROP SEQUENCE public.user_vote_id_seq;
DROP TABLE public.user_subfreddits;
DROP SEQUENCE public.user_subfreddits_id_seq;
DROP SEQUENCE public.user_id_seq;
DROP SEQUENCE public.user_flairs_id_seq;
DROP TABLE public.user_flairs;
DROP SEQUENCE public.subfreddits_moderators_id_seq;
DROP TABLE public.subfreddits_moderators;
DROP SEQUENCE public.subfreddits_id_seq;
DROP TABLE public.subfreddits;
DROP SEQUENCE public.subfreddit_flairs_id_seq;
DROP TABLE public.subfreddit_flairs;
DROP TABLE public.posts;
DROP SEQUENCE public.posts_id_seq;
DROP SEQUENCE public.comments_id_seq;
DROP TABLE public.comments;
DROP SEQUENCE public.chat_messages_id_seq;
DROP TABLE public.chat_messages;
DROP SEQUENCE public.chat_config_id_seq;
DROP TABLE public.chat_config;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


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
    user_id integer NOT NULL,
    sticky integer DEFAULT 0,
    soft_deleted integer DEFAULT 0
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
    description text,
    subscriber_name text DEFAULT 'subscriber'::text NOT NULL,
    header_background text
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

