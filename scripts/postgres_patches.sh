#Only neeeded if we are cleaning sensitive artifacts from a DB.

docker-compose exec -T db \
/bin/bash -c "psql -U postgres issf_prod -f /data/postgres/patches/patch_add_range.sql"

docker-compose exec -T db \
/bin/bash -c "psql -U postgres issf_prod -f /data/postgres/patches/apr22_2020/patch_apr22_2020.sql"

docker-compose exec -T db \
/bin/bash -c "psql -U postgres issf_prod -f /data/postgres/patches/patch_may_10_count.sql"

docker-compose exec -T db \
/bin/bash -c "psql -U postgres issf_prod -f /data/postgres/patches/patch_may_24.sql"

docker-compose exec -T db \
/bin/bash -c "psql -U postgres issf_prod -f /data/postgres/patches/patch_june_6.sql"



