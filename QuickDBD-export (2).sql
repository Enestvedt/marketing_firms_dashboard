-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/WAS4Rr
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "agency" (
    "id" serial   NOT NULL,
    "name" varchar(50)   NOT NULL,
    "city" varchar(30)   NOT NULL,
    "country" varchar(50)   NOT NULL,
    "independent" bool   NOT NULL,
    CONSTRAINT "pk_agency" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "product_category" (
    "id" serial   NOT NULL,
    "name" varchar(50)   NOT NULL,
    CONSTRAINT "pk_product_category" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "agency_product_category" (
    "agency_id" int   NOT NULL,
    "product_category_id" int   NOT NULL,
    CONSTRAINT "pk_agency_product_category" PRIMARY KEY (
        "agency_id","product_category_id"
     )
);

CREATE TABLE "agency_market_rank" (
    "ranking_category" varchar(30)   NOT NULL,
    "year" year   NOT NULL,
    "agency_id" int   NOT NULL,
    "ranking_category_points" int   NOT NULL,
    CONSTRAINT "pk_agency_market_rank" PRIMARY KEY (
        "ranking_category","year","agency_id"
     )
);

CREATE TABLE "brand_market_rank" (
    "ranking_category" varchar(30)   NOT NULL,
    "year" year   NOT NULL,
    "brand" varchar(50)   NOT NULL,
    "product_category_id" int   NOT NULL,
    "points" int   NOT NULL,
    CONSTRAINT "pk_brand_market_rank" PRIMARY KEY (
        "ranking_category","year","brand","product_category_id"
     )
);

ALTER TABLE "agency" ADD CONSTRAINT "fk_agency_id" FOREIGN KEY("id")
REFERENCES "agency_market_rank" ("agency_id");

ALTER TABLE "product_category" ADD CONSTRAINT "fk_product_category_id" FOREIGN KEY("id")
REFERENCES "brand_market_rank" ("product_category_id");

ALTER TABLE "agency_product_category" ADD CONSTRAINT "fk_agency_product_category_agency_id" FOREIGN KEY("agency_id")
REFERENCES "agency" ("id");

ALTER TABLE "agency_product_category" ADD CONSTRAINT "fk_agency_product_category_product_category_id" FOREIGN KEY("product_category_id")
REFERENCES "product_category" ("id");

