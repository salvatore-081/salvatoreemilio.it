package rethinkDB

//   func (rdb *RethinkDB) AddProject(ctx context.Context, in *proto.AddProjectInput) (*proto.Project, error) {

//   wr, e := r.Table(projectsTable).Get()
// 	wr, e := r.Table(usersTable).Insert(in, r.InsertOpts{
// 		ReturnChanges: true,
// 	}).RunWrite(rdb.session)
// 	if e != nil {
// 		if strings.HasPrefix(e.Error(), "Duplicate primary key") {
// 			return new(proto.User), grpc.Errorf(codes.AlreadyExists, fmt.Sprintf("an user with email '%s' already exists", in.Email))
// 		}
// 		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
// 	}

// 	if len(wr.Changes) == 0 {
// 		return new(proto.User), grpc.Errorf(codes.Internal, "unable to read the inserted resource")
// 	}

// 	d, e := json.Marshal(wr.Changes[0].NewValue)
// 	if e != nil {
// 		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
// 	}

// 	u := proto.User{}

// 	e = json.Unmarshal(d, &u)
// 	if e != nil {
// 		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
// 	}

// 	return &u, nil
// }
