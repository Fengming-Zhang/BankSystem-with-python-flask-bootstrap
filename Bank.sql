/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/4/30 17:02:06                           */
/*==============================================================*/

drop database if exists Bank;
create database Bank;
use Bank;


-- alter table 付款 
--    drop foreign key FK_付款_逐次支付_贷款;

-- alter table 使用账户 
--    drop foreign key FK_使用账户_使用账户_客户;

-- alter table 使用账户 
--    drop foreign key FK_使用账户_使用账户2_账户;

-- alter table 借贷 
--    drop foreign key FK_借贷_借贷_贷款;

-- alter table 借贷 
--    drop foreign key FK_借贷_借贷2_客户;

-- alter table 储蓄账户 
--    drop foreign key FK_储蓄账户_储蓄类_账户;

-- alter table 员工 
--    drop foreign key FK_员工_属于_部门;

-- alter table 客户 
--    drop foreign key FK_客户_客户联系人_联系人;

-- alter table 支票账户 
--    drop foreign key FK_支票账户_支票类_账户;

-- alter table 账户 
--    drop foreign key FK_账户_开户_支行;

-- alter table 账户 
--    drop foreign key FK_账户_账户负责人_员工;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束_支行;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束2_客户;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束3_储蓄账户;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束4_支票账户;

-- alter table 贷款 
--    drop foreign key FK_贷款_发放_支行;

-- alter table 贷款 
--    drop foreign key FK_贷款_贷款负责人_员工;

-- alter table 部门 
--    drop foreign key FK_部门_下设_支行;

-- alter table 部门 
--    drop foreign key FK_部门_管理2_部门经理;

-- alter table 部门经理 
--    drop foreign key FK_部门经理_管理_部门;

-- alter table 部门经理 
--    drop foreign key FK_部门经理_领导_员工;


-- alter table 付款 
--    drop foreign key FK_付款_逐次支付_贷款;

-- drop table if exists 付款;


-- alter table 使用账户 
--    drop foreign key FK_使用账户_使用账户_客户;

-- alter table 使用账户 
--    drop foreign key FK_使用账户_使用账户2_账户;

-- drop table if exists 使用账户;


-- alter table 借贷 
--    drop foreign key FK_借贷_借贷_贷款;

-- alter table 借贷 
--    drop foreign key FK_借贷_借贷2_客户;

-- drop table if exists 借贷;


-- alter table 储蓄账户 
--    drop foreign key FK_储蓄账户_储蓄类_账户;

-- drop table if exists 储蓄账户;


-- alter table 员工 
--    drop foreign key FK_员工_属于_部门;

-- drop table if exists 员工;


-- alter table 客户 
--    drop foreign key FK_客户_客户联系人_联系人;

-- drop table if exists 客户;


-- alter table 支票账户 
--    drop foreign key FK_支票账户_支票类_账户;

-- drop table if exists 支票账户;

-- drop table if exists 支行;

-- drop table if exists 联系人;


-- alter table 账户 
--    drop foreign key FK_账户_开户_支行;

-- alter table 账户 
--    drop foreign key FK_账户_账户负责人_员工;

-- drop table if exists 账户;


-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束_支行;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束2_客户;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束3_储蓄账户;

-- alter table 账户约束 
--    drop foreign key FK_账户约束_账户约束4_支票账户;

-- drop table if exists 账户约束;


-- alter table 贷款 
--    drop foreign key FK_贷款_发放_支行;

-- alter table 贷款 
--    drop foreign key FK_贷款_贷款负责人_员工;

-- drop table if exists 贷款;


-- alter table 部门 
--    drop foreign key FK_部门_管理2_部门经理;

-- alter table 部门 
--    drop foreign key FK_部门_下设_支行;

-- drop table if exists 部门;


-- alter table 部门经理 
--    drop foreign key FK_部门经理_管理_部门;

-- alter table 部门经理 
--    drop foreign key FK_部门经理_领导_员工;

-- drop table if exists 部门经理;


/*==============================================================*/
/* Table: 付款                                                    */
/*==============================================================*/
create table 付款
(
   贷款号                  varchar(22) not null  comment '',
   时间                   datetime not null  comment '',
   贷款ID                 varchar(22)  comment '',
   金额                   float(10) not null  comment '',
   primary key (贷款号, 时间)
);

/*==============================================================*/
/* Table: 使用账户                                                  */
/*==============================================================*/
create table 使用账户
(
   UserID               varchar(22) not null  comment '',
   账户ID                 varchar(22) not null  comment '',
   使用时间                 datetime  comment '',
   primary key (UserID, 账户ID, 使用时间)
);

/*==============================================================*/
/* Table: 借贷                                                    */
/*==============================================================*/
create table 借贷
(
   贷款ID                 varchar(22) not null  comment '',
   UserID               varchar(22) not null  comment '',
   primary key (贷款ID, UserID)
);

/*==============================================================*/
/* Table: 储蓄账户                                                  */
/*==============================================================*/
create table 储蓄账户
(
   账户ID                 varchar(22) not null  comment '',
   支行Name               varchar(10)  comment '',
   StaffID              varchar(22)  comment '',
   账户类型                 varchar(10) not null  comment '',
   余额                   float(10) not null  comment '',
   开户日期                 date not null  comment '',
   开户支行                 varchar(10) not null  comment '',
   利率                   float(10)  comment '',
   primary key (账户ID)
);

/*==============================================================*/
/* Table: 员工                                                    */
/*==============================================================*/
create table 员工
(
   StaffID              varchar(22) not null  comment '',
   DepartmentID         varchar(10) not null  comment '',
   姓名                   varchar(10) not null  comment '',
   电话号码                 varchar(16) not null  comment '',
   家庭住址                 varchar(30) not null  comment '',
   开始工作日期               date not null  comment '',
   primary key (StaffID)
);

/*==============================================================*/
/* Table: 客户                                                    */
/*==============================================================*/
create table 客户
(
   UserID               varchar(22) not null  comment '',
   联系人手机号               varchar(16) not null  comment '',
   姓名                   varchar(10) not null  comment '',
   联系电话                 varchar(16) not null  comment '',
   家庭住址                 varchar(30) not null  comment '',
   联系人客户关系              varchar(10) not null  comment '',
   primary key (UserID)
);

/*==============================================================*/
/* Table: 支票账户                                                  */
/*==============================================================*/
create table 支票账户
(
   账户ID                 varchar(22) not null  comment '',
   支行Name               varchar(10)  comment '',
   StaffID              varchar(22)  comment '',
   账户类型                 varchar(10) not null  comment '',
   余额                   float(10) not null  comment '',
   开户日期                 date not null  comment '',
   开户支行                 varchar(10) not null  comment '',
   货币类型                 varchar(10)  comment '',
   透支额                  float(10)  comment '',
   primary key (账户ID)
);

/*==============================================================*/
/* Table: 支行                                                    */
/*==============================================================*/
create table 支行
(
   支行Name               varchar(10) not null  comment '',
   资产                   float(10) not null  comment '',
   primary key (支行Name)
);

/*==============================================================*/
/* Table: 联系人                                                   */
/*==============================================================*/
create table 联系人
(
   姓名                   varchar(10) not null  comment '',
   手机号                  varchar(16) not null  comment '',
   Email                varchar(30) not null  comment '',
   primary key (手机号)
);

/*==============================================================*/
/* Table: 账户                                                    */
/*==============================================================*/
create table 账户
(
   账户ID                 varchar(22) not null  comment '',
   支行Name               varchar(10) not null  comment '',
   StaffID              varchar(22)  comment '',
   账户类型                 varchar(10) not null  comment '',
   余额                   float(10) not null  comment '',
   开户日期                 date not null  comment '',
   开户支行                 varchar(10) not null  comment '',
   primary key (账户ID)
);

/*==============================================================*/
/* Table: 账户约束                                                  */
/*==============================================================*/
create table 账户约束
(
   支行Name               varchar(10) not null  comment '',
   UserID               varchar(22) not null  comment '',
   储蓄账户ID               varchar(22)  comment '',
   支票账户ID               varchar(22)  comment '',
   primary key (支行Name, UserID)
);

/*==============================================================*/
/* Table: 贷款                                                    */
/*==============================================================*/
create table 贷款
(
   贷款ID                 varchar(22) not null  comment '',
   StaffID              varchar(22)  comment '',
   支行Name               varchar(10) not null  comment '',
   金额                   float(10) not null  comment '',
   支付方式                 varchar(10) not null  comment '',
   primary key (贷款ID)
);

/*==============================================================*/
/* Table: 部门                                                    */
/*==============================================================*/
create table 部门
(
   DepartmentID         varchar(10) not null  comment '',
   支行Name               varchar(10) not null  comment '',
   StaffID              varchar(22)  comment '',
   部门名称                 varchar(10) not null  comment '',
   部门类型                 varchar(10) not null  comment '',
   部门经理ID               varchar(22) not null  comment '',
   primary key (DepartmentID)
);

/*==============================================================*/
/* Table: 部门经理                                                  */
/*==============================================================*/
create table 部门经理
(
   StaffID              varchar(22) not null  comment '',
   DepartmentID         varchar(10) not null  comment '',
   部门_DepartmentID      varchar(10)  comment '',
   姓名                   varchar(10) not null  comment '',
   电话号码                 varchar(16) not null  comment '',
   家庭住址                 varchar(30) not null  comment '',
   开始工作日期               date not null  comment '',
   primary key (StaffID)
);

alter table 付款 add constraint FK_付款_逐次支付_贷款 foreign key (贷款ID)
      references 贷款 (贷款ID) on delete restrict on update restrict;

alter table 使用账户 add constraint FK_使用账户_使用账户_客户 foreign key (UserID)
      references 客户 (UserID) on delete restrict on update restrict;

alter table 使用账户 add constraint FK_使用账户_使用账户2_账户 foreign key (账户ID)
      references 账户 (账户ID) on delete restrict on update restrict;

alter table 借贷 add constraint FK_借贷_借贷_贷款 foreign key (贷款ID)
      references 贷款 (贷款ID) on delete restrict on update restrict;

alter table 借贷 add constraint FK_借贷_借贷2_客户 foreign key (UserID)
      references 客户 (UserID) on delete restrict on update restrict;

alter table 储蓄账户 add constraint FK_储蓄账户_储蓄类_账户 foreign key (账户ID)
      references 账户 (账户ID) on delete restrict on update restrict;

alter table 员工 add constraint FK_员工_属于_部门 foreign key (DepartmentID)
      references 部门 (DepartmentID) on delete restrict on update restrict;

alter table 客户 add constraint FK_客户_客户联系人_联系人 foreign key (联系人手机号)
      references 联系人 (手机号) on delete restrict on update restrict;

alter table 支票账户 add constraint FK_支票账户_支票类_账户 foreign key (账户ID)
      references 账户 (账户ID) on delete restrict on update restrict;

alter table 账户 add constraint FK_账户_开户_支行 foreign key (支行Name)
      references 支行 (支行Name) on delete restrict on update restrict;

alter table 账户 add constraint FK_账户_账户负责人_员工 foreign key (StaffID)
      references 员工 (StaffID) on delete restrict on update restrict;

alter table 账户约束 add constraint FK_账户约束_账户约束_支行 foreign key (支行Name)
      references 支行 (支行Name) on delete restrict on update restrict;

alter table 账户约束 add constraint FK_账户约束_账户约束2_客户 foreign key (UserID)
      references 客户 (UserID) on delete restrict on update restrict;

alter table 账户约束 add constraint FK_账户约束_账户约束3_储蓄账户 foreign key (储蓄账户ID)
      references 储蓄账户 (账户ID) on delete restrict on update restrict;

alter table 账户约束 add constraint FK_账户约束_账户约束4_支票账户 foreign key (支票账户ID)
      references 支票账户 (账户ID) on delete restrict on update restrict;

alter table 贷款 add constraint FK_贷款_发放_支行 foreign key (支行Name)
      references 支行 (支行Name) on delete restrict on update restrict;

alter table 贷款 add constraint FK_贷款_贷款负责人_员工 foreign key (StaffID)
      references 员工 (StaffID) on delete restrict on update restrict;

alter table 部门 add constraint FK_部门_下设_支行 foreign key (支行Name)
      references 支行 (支行Name) on delete restrict on update restrict;

alter table 部门 add constraint FK_部门_管理2_部门经理 foreign key (StaffID)
      references 部门经理 (StaffID) on delete restrict on update restrict;

alter table 部门经理 add constraint FK_部门经理_管理_部门 foreign key (DepartmentID)
      references 部门 (DepartmentID) on delete restrict on update restrict;

alter table 部门经理 add constraint FK_部门经理_领导_员工 foreign key (StaffID)
      references 员工 (StaffID) on delete restrict on update restrict;

insert into 联系人 (姓名, 手机号, Email)
			values
            ('王五', 112, '12345@test.cn');
            
insert into 支行 (支行name, 资产)
			values
            ('西安碑林支行', 12000000.0);

insert into 部门 (DepartmentID, 支行name, 部门名称, 部门类型, 部门经理ID)
			values
            ('003', '西安雁塔支行', '业务部', '业务类', '001');

insert into 员工 (StaffID, DepartmentID, 姓名, 电话号码, 家庭住址, 开始工作日期)
			values
			('020', '003', '快银', '171', '西安市雁塔区', '2020-02-01');
            
show tables;
show table status;
select * from 客户;
select * from 联系人;
select * from 支行;
select * from 部门;
select * from 员工;
select * from 账户;
select * from 储蓄账户; 
select * from 支票账户;
select * from 账户约束;
select * from 使用账户;
select * from 借贷;
select * from 贷款;
select * from 付款;
update 账户约束 set 支票账户ID = null where userID = '0001';
delete from 账户 where 账户ID = '0001';
update 支票账户 set 透支额 = 0 where 账户ID = '0001';
update 账户 set StaffID = '001' where 账户ID = '0001';
update 支行 set 资产 = 10000000 where 支行Name = '西安支行';
delete from 付款 where 贷款ID = '1000';
insert into 使用账户 values ('0001', '0001', '2020-06-30');