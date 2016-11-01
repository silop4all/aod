set @user = "user";
--
select id into @user_id from app_users where username=@user;
select @user_id;
select id into @consumer_id from app_consumers where user_id=@user_id;
select id into @carer_id from app_carers where user_id=@user_id;
select id into @provider_id from app_providers where user_id=@user_id;
--
delete from app_oauth2_tokens where user_id=@user_id;
delete from app_carers where user_id=@user_id;
delete from app_consumers where user_id=@user_id;
delete from app_providers where user_id=@user_id;
delete from app_carers_assist_consumers where consumer_id=@consumer_id;
delete from app_nas_temp_setup where consumer_id=@consumer_id;
delete from app_consumers_services where consumer_id=@consumer_id;
delete from app_nas_consumers_services where consumer_id=@consumer_id;
delete from app_nas_temp_setup where carer_id=@carer_id;
delete from app_carers_assist_consumers where carer_id=@carer_id;
delete from app_services where owner_id=@provider_id;
delete from users where id=@user_id;