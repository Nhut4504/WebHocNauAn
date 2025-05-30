PGDMP      +                }         	   Hocnauan1    17.4    17.4 5    _           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            `           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            a           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            b           1262    16389 	   Hocnauan1    DATABASE     q   CREATE DATABASE "Hocnauan1" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en-US';
    DROP DATABASE "Hocnauan1";
                     postgres    false            �            1255    24658    update_post_updated_at()    FUNCTION     �   CREATE FUNCTION public.update_post_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$;
 /   DROP FUNCTION public.update_post_updated_at();
       public               postgres    false            �            1255    24640    update_updated_at_column()    FUNCTION     �   CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$;
 1   DROP FUNCTION public.update_updated_at_column();
       public               postgres    false            �            1259    16391    category    TABLE     t   CREATE TABLE public.category (
    categoryid integer NOT NULL,
    categoryname character varying(100) NOT NULL
);
    DROP TABLE public.category;
       public         heap r       postgres    false            �            1259    16390    category_categoryid_seq    SEQUENCE     �   CREATE SEQUENCE public.category_categoryid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.category_categoryid_seq;
       public               postgres    false    218            c           0    0    category_categoryid_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.category_categoryid_seq OWNED BY public.category.categoryid;
          public               postgres    false    217            �            1259    24643    posts    TABLE     N  CREATE TABLE public.posts (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    image_path character varying(255)
);
    DROP TABLE public.posts;
       public         heap r       postgres    false            �            1259    24642    posts_id_seq    SEQUENCE     �   CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.posts_id_seq;
       public               postgres    false    228            d           0    0    posts_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;
          public               postgres    false    227            �            1259    16396    product    TABLE     Z  CREATE TABLE public.product (
    productid integer NOT NULL,
    categoryid integer,
    productname character varying(255) NOT NULL,
    imageurl text,
    note text,
    rating numeric(3,2),
    instructions text,
    ingredient_tips text,
    CONSTRAINT product_rating_check CHECK (((rating >= (0)::numeric) AND (rating <= (5)::numeric)))
);
    DROP TABLE public.product;
       public         heap r       postgres    false            �            1259    16395    product_productid_seq    SEQUENCE     ~   CREATE SEQUENCE public.product_productid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.product_productid_seq;
       public               postgres    false    220            e           0    0    product_productid_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.product_productid_seq OWNED BY public.product.productid;
          public               postgres    false    219            �            1259    16404    recipe_steps    TABLE     �   CREATE TABLE public.recipe_steps (
    id integer NOT NULL,
    product_id integer,
    step_number integer,
    instruction text,
    image_url text,
    video_url text
);
     DROP TABLE public.recipe_steps;
       public         heap r       postgres    false            �            1259    16403    recipe_steps_id_seq    SEQUENCE     |   CREATE SEQUENCE public.recipe_steps_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.recipe_steps_id_seq;
       public               postgres    false    222            f           0    0    recipe_steps_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.recipe_steps_id_seq OWNED BY public.recipe_steps.id;
          public               postgres    false    221            �            1259    16411    recipes    TABLE     �   CREATE TABLE public.recipes (
    id integer NOT NULL,
    name text NOT NULL,
    ingredients text NOT NULL,
    instructions text NOT NULL,
    image_url text,
    ingredient_tips text,
    video_url text
);
    DROP TABLE public.recipes;
       public         heap r       postgres    false            �            1259    16410    recipes_id_seq    SEQUENCE     w   CREATE SEQUENCE public.recipes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.recipes_id_seq;
       public               postgres    false    224            g           0    0    recipes_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;
          public               postgres    false    223            �            1259    24624    users    TABLE        CREATE TABLE public.users (
    id integer NOT NULL,
    full_name character varying(255) NOT NULL,
    account character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    role character varying(50) DEFAULT 'user'::character varying,
    status character varying(50) DEFAULT 'active'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    24623    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               postgres    false    226            h           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               postgres    false    225            �           2604    16435    category categoryid    DEFAULT     z   ALTER TABLE ONLY public.category ALTER COLUMN categoryid SET DEFAULT nextval('public.category_categoryid_seq'::regclass);
 B   ALTER TABLE public.category ALTER COLUMN categoryid DROP DEFAULT;
       public               postgres    false    218    217    218            �           2604    24646    posts id    DEFAULT     d   ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);
 7   ALTER TABLE public.posts ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    227    228            �           2604    16436    product productid    DEFAULT     v   ALTER TABLE ONLY public.product ALTER COLUMN productid SET DEFAULT nextval('public.product_productid_seq'::regclass);
 @   ALTER TABLE public.product ALTER COLUMN productid DROP DEFAULT;
       public               postgres    false    220    219    220            �           2604    16437    recipe_steps id    DEFAULT     r   ALTER TABLE ONLY public.recipe_steps ALTER COLUMN id SET DEFAULT nextval('public.recipe_steps_id_seq'::regclass);
 >   ALTER TABLE public.recipe_steps ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    222    221    222            �           2604    16438 
   recipes id    DEFAULT     h   ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);
 9   ALTER TABLE public.recipes ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    223    224    224            �           2604    24627    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    225    226    226            R          0    16391    category 
   TABLE DATA           <   COPY public.category (categoryid, categoryname) FROM stdin;
    public               postgres    false    218   �>       \          0    24643    posts 
   TABLE DATA           `   COPY public.posts (id, title, content, user_id, created_at, updated_at, image_path) FROM stdin;
    public               postgres    false    228   ?       T          0    16396    product 
   TABLE DATA           |   COPY public.product (productid, categoryid, productname, imageurl, note, rating, instructions, ingredient_tips) FROM stdin;
    public               postgres    false    220   >G       V          0    16404    recipe_steps 
   TABLE DATA           f   COPY public.recipe_steps (id, product_id, step_number, instruction, image_url, video_url) FROM stdin;
    public               postgres    false    222   �K       X          0    16411    recipes 
   TABLE DATA           m   COPY public.recipes (id, name, ingredients, instructions, image_url, ingredient_tips, video_url) FROM stdin;
    public               postgres    false    224   �O       Z          0    24624    users 
   TABLE DATA           n   COPY public.users (id, full_name, account, password, email, role, status, created_at, updated_at) FROM stdin;
    public               postgres    false    226   �Y       i           0    0    category_categoryid_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.category_categoryid_seq', 1, false);
          public               postgres    false    217            j           0    0    posts_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.posts_id_seq', 60, true);
          public               postgres    false    227            k           0    0    product_productid_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.product_productid_seq', 4, true);
          public               postgres    false    219            l           0    0    recipe_steps_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.recipe_steps_id_seq', 9, true);
          public               postgres    false    221            m           0    0    recipes_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.recipes_id_seq', 3, true);
          public               postgres    false    223            n           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 5, true);
          public               postgres    false    225            �           2606    24652    posts posts_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_pkey;
       public                 postgres    false    228            �           2606    16443    product product_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (productid);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public                 postgres    false    220            �           2606    16445    recipe_steps recipe_steps_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.recipe_steps
    ADD CONSTRAINT recipe_steps_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.recipe_steps DROP CONSTRAINT recipe_steps_pkey;
       public                 postgres    false    222            �           2606    16447    recipes recipes_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.recipes DROP CONSTRAINT recipes_pkey;
       public                 postgres    false    224            �           2606    24637    users users_account_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_account_key UNIQUE (account);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_account_key;
       public                 postgres    false    226            �           2606    24639    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    226            �           2606    24635    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    226            �           2620    24659 $   posts trigger_update_post_updated_at    TRIGGER     �   CREATE TRIGGER trigger_update_post_updated_at BEFORE UPDATE ON public.posts FOR EACH ROW EXECUTE FUNCTION public.update_post_updated_at();
 =   DROP TRIGGER trigger_update_post_updated_at ON public.posts;
       public               postgres    false    230    228            �           2620    24641 $   users trigger_update_user_updated_at    TRIGGER     �   CREATE TRIGGER trigger_update_user_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
 =   DROP TRIGGER trigger_update_user_updated_at ON public.users;
       public               postgres    false    229    226            �           2606    24653    posts posts_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
 B   ALTER TABLE ONLY public.posts DROP CONSTRAINT posts_user_id_fkey;
       public               postgres    false    228    4793    226            �           2606    16454 )   recipe_steps recipe_steps_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.recipe_steps
    ADD CONSTRAINT recipe_steps_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(productid);
 S   ALTER TABLE ONLY public.recipe_steps DROP CONSTRAINT recipe_steps_product_id_fkey;
       public               postgres    false    220    4783    222            R   9   x�3��=�9O!9���|.S'��¼.C�L��Uy\F^���\�P�D��=... �T�      \   )  x��XMoW];���z�:�C>6Q?Hm�4��x�z�x��=��])��
E��E7B�@ H�3B]L���@�z�}o�vHS���{��w�9瞡�\YϞ�lW���n���+�̓��z��=u�݋wC�R7��6�D��ƚ=�Nni�u��?F��c��Z�}ur���ɟ�vT���K_eC�W}w�=O��<���s��J�:�Q~��U���L�A`���=������0�G��H���	E��a��y��W�=Y����V!N�\���dPU_�׿��GX�P#!��~�$�C9�Y�4�?�LVbb-�����h����*/�ǻ��J�ʆ��N~Fɱ��H��z9����ƶIm�~&y?Y���0&�;�g. t�d�k��H��<y�����q���_i~U}�'C~���A���K�Lr	M2��=�쮩+����νFu��ˎm�r�<��M��H���@��]z(��3����������O*�J�V_�����|C�/�.,�.,T�j���y��^�k�T>�-��#I����%p�?�'��j���Y��V��ۯ,�������bY������T�)�0�.0���-z��>�m�c��A�����Ln��G�걗�B���TЫ���7C��A��O@Ϻ���b�p�!xq�V�1$Q^��`�,�	��O؁R�@��ܜ�hT��(,y��΄uύ�^��X��P#��}%�6igCD�]<A�Iw6�iHt�;,V2��e_)h�vY��-��)���O���6��&�a7�e���M����1ju���cW��(�z8�7�:�����_(��	㘅au;{���Ȗ`d���ᙴ��Z_�6��j�>�k���b/bd�z�ъ6Y�Fn��ɛ���vǖ�ˆ�a����������9�K��(?����.��������<Hq�*��� �}(�$�R���\����m~�L$ǔc����=æ�!8vv�0`�=	gH*�B��tfTUW��U]K]tu\t,���]�Fxf�2U}��c& #S,�x�7�mW��`��Wի����o�/I�_�ys���1�
�v��I�����̞ȅ��椿N1�p�g.#>�%Fz���s�!��>�����[*�k8ŐbU~u�qƱ�D�C#�|�<0s�tyț�4A�.�gz�	eL��������Aid(!�4�g%EӒH弲�_������L_6� cL�Nm�6S����mgav�V۱i����e����іKJ>4(:}�������>��RS��^�0!7D�'2WN�����9�D�A�4V>�j�ݑ��X������?0,T�߾�:����;V���Lf�C�ZZm�W+���{D՚�|&����件�3��N���b�_��q�7G����e��p��Dy�,o�� ��J��>���S���8@�1M3�k�S%�:L&󃦒�APP�t%/�҉�;QaTC_9�H�ֈ�������:��ҳ��h'�g����b�Ej-d�.-��E]����(�i��P+��7]k�=Mm1p�R����~ �暲�,Xw�Z8�4�*2m�F��@�Rp�3�ݡ�I
6t}�����9�]�*�/����)G,��iO��b��'�\����ALSD&�����6ߗ��}2�T9����|�������Q?bB�Go�ߑ,�!bON�xy;���)93��wg�{C�b.���IӨ3/�^f��k����L���;�����bD��}(\A$�㘉r
5=�62.�<�yaˎ;���B	�W���
�1i���Y(e���Gy8�y�Cۘ�q+�yw�U%���pyuq�������8��^���'��>��f"��hX�kG\��[{,��Qv#�&�i��X`|r��$B�Z�R��=[S//�[��`�w�@�,��f�>&U*�W9�����^j��s�+�u*��*<}9���@�X�jA8�)�0	���90���,��]����x�w�W%���є��03��u��˪V_m,��/Á��k��{w�w��q8�	�o����չ��\�l=      T   e  x�uVMo�F=ӿb��2���VGۇ�i}�9�B�.�Z\*�Ұo5��(��z(*U0'l$�(rXC���%}�\*��%�ξy�ffG5�f���yA�^�A�κ���udyq��#a����]5��l�� �^,|�5��TZ[v�j�lGj5��=m��sE��ul}���.��o��O�����8�Z�J~�X���[��ti�^$y:�MO�c��K��ٌ��
V�-�Ny�=~	?���.q�~�X��ٯ���(�L��4�@��7�����57ڄ%/�N�`��@�pI��u��M��1��E�R]w�9V�9�K��<�am�$�� P�#�X�Ҳ��v��_�f'φ���+��$�� Oͤ#jU����4���bً>���.|%��
�Ð���'�������F!�F$O-�
߲��#��x��O�����{3O��zC>0b�H��S�ƥ����
}���PUl�~Ңg�N�D�����S�Bm$���|��>�:Tw� �� nX�h�s��l+����/�D�����Y����g��n�s>�3n��a�fU�c��T��ￗI豉_���xh�uOǁ^�܂Q�NU��1�
��D*�~�Dй�,j����3*ԇ�� M��aӞ���6t�y)��D�w�7�>� X��ŵ�aQ��q�e�M�I\�Xx�������z�fH�ɒ��]lL}�pCr��殦�jp�ʩ���G�)��2Z>Т}V��NX��r=O���� ��"u�*�_-�nX؟'eFX�Ǌ�@�ԈI��]wU7�� 8�W�t�6_Qe�����H+s�6|�a�ST�>�����)]En�XVt~�0%p���pjx��Q�q��|5Ҏ��ř�X�� �ry�����g��bIY\1j$��/ʞ�.֝�]���韢���i1P�.�H_�EC���4�<�c�\<([ߐn����/��(��)�E[��z����љZZ��Rg���U��E�hS�3��L���ܰ�>���#�]4K[V��ŀ@5Ů�jl��Я�C櫦�^]�	X 7�-kwQ��Y^�ƾ� ��/qV�L8�V������WXm��P��:��`{cc�?#$-�      V   �  x�}TMo�F=S�bz'hX�H�[��
b�P�� �6WL���c=EcE�PF`ȩ�&�%$�V���?��eD9J/��ݙy�͛��6���`QR�4�[�M�g�F�q��?{�o.���>�5U�h��?k:i�_|>��4�y��7�KMHUj:n�WE@�M5+�a1l�#�������⯦���Ѣ\MF'��^>R	G�����U@���N̟���E��qf��%*����uP�5rTV�����]0�)b5�hl.���/gq�U�r5����!�7jJ��F���с�᪳��s�� 3U��$,pgnq8fj7mRV4���� �)']8���N�MA��3)Ч�����NC��� ��� �7\�ؼ�"2� x�':�V�e��!+��:�Tv��
��E���}-�؋���w8� w��6��FMu5xW���V�Q����ܾ�V�k�8܇(+Q�YgQf�(���X�+-Z��}�-��;f��Wk�*��@�8������g�|��� ���q��\#���ef�Y\��[�B�o?I90I�������b~.�1�Εm��D���1.���P�5�'zQ��Cq��?���US�9p%��c���o�HFS�����}��vF�f%;6����9��,?K�Ĕ- }�/��tw\������̴�I1����	a�^t�1��,�������q�w��}�+��.U��`�u�=�`�;H�%��67�t�[k���;ͤK�5����W�5����̼i�1�s��hZS_�mK����Dk�p(#����Ǆ6k���X�r����ח�|9���UR��(��&��;��*�h�5�EL����_��֋�*si�%�'Y�ir���6[?6l�[J�6T|�Ѳ[����[����Pl�'w�t����G�=�q��hH�5��D�|���qzz��W�l�hx�1�~��N_}��^�?$��      X   
  x��Y]o�}�~�<�iM[R�&� R��-8�
8�_ȕ�݊;d�]}��1� 
E0��-���X����@$
=�����%=�ޙ��e�� ,�ܝ�s?�=sf�Nm�t�8�F��pЕϞ���E6��V����n{j&}�� ������/��s�����y��(D�L�v6�[\���D����:=�О��/�Vd]O�J�#�J��_^t6H��V�l���7u�P����-���:���̋2�����5��ͨ��^�vo�&�jw��;LxY[ħ�c�H�`�G�<5�n�K'xj��� �O��醧n��@�le�oɻ�<�������F��V�0}�ȳ���2���O�6�r�4�A	x��n6���q:i�����œ�l���f��yh���=4i��Rz�wR�ɪuC݂�A��g*&���ʎD4��L�f�������� b��ﱧ�y�hꍰ�VxC}$���#L���]���9��G*y�$;J(Fjg,K�m8�>Ӵ�̦��%��W���N��h�Y[�K�j0�Q��"�p���ZIC���\6�TQz��C��BH�J_)2���Xi<ڍ�u����������l�3C �N�L�O�k��̚��n3�+1z�2>s�y�麚O���Q5e��z�z�φ�em�W�]�\��:E�1ڄ`T7)LJ��
JM��:w�M����P��={q���"�J��@Z��b�Yk�����E�m�� "cO��/b�^�mu��� (��J��x��U:��a�̊����·�����a�u�[�Y��8�����\f!��*+0ҁ�������f�}��?%6 J�ܦ�ٴBoC�Z�]ױk�A�"uǁy\�Rn��08��9��#� �R����2��]?�J��{}��L׬��o�!B��)�i榒 �%J��q�S���}�ᑈ�MV'��s����(w��Z�Hm�����K��+M���Q�wʖ6�)�)��/&L�9�\(�
�x�5,�B.&
�p>�kA�VW�����7�I����!�5c?xo���7>�k�^�l������HR�E'��G�1X�$�\�����$*��u�= n3,�c?����0)��\V{������=V~�SC-�^�01���h�&v54�*gD��6g[��1�Mc�����@(��o,�Z�m؆:�&т-�B��96Bd��,z�8���e�h�(�c���N�eś����B˽N������Hg��P}"{:^��{�������0��݂�:���Fv������O���/ӡ.2*)�D�I����g������[aqI�)0���\n_֥ �a{��]S��8ֲ�شH#�[tZ�pD�+�������X�@�*�@��B-@�hӑ�>j7�R:LG}�u#r��b�D�E������ߺ^k%��O�Jͺ��j �+xܾ�m�7)��l�O�h?H��S���C^�{�t����a�4��I���Hs��W�
(���QM�N��\�Ў�s�M�Y�v���A�}��Y��%d% �n���y�9�e%M�� !���jW]�����ƫ�\�P����j"���L�KpEN%��^f�R�e�,X̌9B�B�]���hrNq9�ȁ���I�K��It���%<ֳz��d�r8��ٿN:�]�3��c��T ���� �.�*Ѯ�݊�‮`�W�R�z^�IEm�Hb�Ҏ�U����jS.)�0����;��g��JR�� ���Sh�k���'�T�]pq�J���v��xt����8[:�Y�Z(��Ejkv����ڻ���ǉ���l�_H_�8��8���T��:鳮��������P�q�M���;(Z��Z˗+�D��?������'~_���u�S�a�j��+N�9i	`
y��r�)�+�Vn�r��)�u{Y���+<�g^TN%�d�ní/�-l�<��jgw�C��Q�������k�}���ҁg�˧��
ҧZk�[^� Z3.���q$N�NF��'���p��+Z�Y�БF�?U)t$�����r��$w��v�K(1������]�]�l9��i���*R�2�xE��$�6�Y�.%ЃI.;� KǥB3�3���A���gnZ��0�G�=�xh/}���x9�R�nƫ>�c��ˍ�y���yK�* �7����Ş9�4HEC��/�#|[��_��XU@�MeLcu�0�hq���=M
�qو�1-[:��������36+.9����v.X�M���T�s��*����Ff��ޑl�nX�e�Y\�G���Qwn��V$o�FH��}�<�����*�0�w�F��������u�#.�	�huS�9�M[�N@p�J�MCN�
�klc���M�^��VI��ts�
*�%�PV�S��R(Y�QǤ�9��x9�ȩ;��)�#C>U����t�z�+5����p�ō�7���`|``-)��(4�5`�K��E��<�.<�P��\���;
e��B������������É{������#      Z   �   x���=N1���)|�X����M*$��4�M[��v��#�(%�����&� ��Ba�����7�K�Ƈ��CC������P�,����l�5ᆵ��U"4m�k\��3T���I�P�Z��-�P1�R��إ�)ҋ=]����a�S2�	m�]�~�Y�43VZ��P(�_����`2_9�SR�Q�v���-���䗗ǿv�����d��?,�!�t|�������pø�m̈́E�!��g��     